"""Input validation shared by UI and integrations."""
import ipaddress
import re
from email_validator import validate_email, EmailNotValidError


def domain_name(value):
    value = value.strip().rstrip('.')
    try:
        ipaddress.ip_address(value)
    except ValueError:
        pass
    else:
        raise ValueError('Enter a domain name, not an IP address.')
    try:
        value = value.encode('idna').decode('ascii').lower()
    except UnicodeError as exc:
        raise ValueError('Invalid international domain name.') from exc
    labels = value.split('.')
    if len(value) > 253 or len(labels) < 2 or any(
        not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', x) for x in labels
    ) or labels[-1].isdigit():
        raise ValueError('Enter a domain such as example.com, without a URL or path.')
    return value


def email_address(value):
    try:
        return validate_email(value.strip(), check_deliverability=False).normalized
    except EmailNotValidError as exc:
        raise ValueError(str(exc)) from exc


def username(value):
    value = value.strip()
    if not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.-]{0,63}', value):
        raise ValueError('Use 1–64 letters, digits, underscores, dots or hyphens; start with a letter, digit or underscore.')
    return value
