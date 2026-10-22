"""Breach metadata via the official HIBP API; no passwords or dump scraping."""
from urllib.parse import quote
import requests
from modules.utils import email_address


def check_breaches(value, api_key, get=None):
    email = email_address(value)
    if not api_key or not api_key.strip():
        raise ValueError('Set HIBP_API_KEY or enter your HIBP API key in the sidebar.')
    get = get or requests.get
    try:
        response = get('https://haveibeenpwned.com/api/v3/breachedaccount/' + quote(email, safe=''),
                       headers={'hibp-api-key': api_key.strip(), 'user-agent': 'InfoHawk/4.0'},
                       params={'truncateResponse': 'false'}, timeout=(5, 20), allow_redirects=False)
    except requests.RequestException:
        return {'status': 'connection_failed', 'message': 'Could not reach HIBP. Check your connection and try again.'}
    if response.status_code == 404:
        return {'status': 'not_found', 'email': email, 'breaches': [],
                'note': 'No record returned by HIBP; this does not prove the account is secure.'}
    if response.status_code == 429:
        return {'status': 'rate_limited', 'retry_after_seconds': response.headers.get('Retry-After'),
                'message': 'Wait before retrying; your HIBP subscription rate limit was reached.'}
    if response.status_code != 200:
        messages = {401: 'Invalid or missing API key.', 403: 'Request forbidden; check your HIBP subscription.',
                    400: 'HIBP rejected the request.'}
        return {'status': 'api_error', 'http_status': response.status_code,
                'message': messages.get(response.status_code, 'HIBP is unavailable or returned an unexpected response.')}
    try:
        payload = response.json()
        if not isinstance(payload, list) or any(not isinstance(b, dict) for b in payload):
            raise ValueError('Unexpected response')
    except ValueError:
        return {'status': 'invalid_response', 'message': 'HIBP returned an unexpected response.'}
    fields = ('Name', 'Title', 'Domain', 'BreachDate', 'AddedDate', 'DataClasses', 'IsVerified', 'IsSensitive')
    return {'status': 'ok', 'email': email,
            'breaches': [{k: b.get(k) for k in fields} for b in payload],
            'source': 'https://haveibeenpwned.com/API/v3'}
