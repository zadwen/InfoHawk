from modules.utils import email_address
from modules.domainrecon import lookup


def analyze(value):
    email = email_address(value)
    domain = email.rsplit('@', 1)[1]
    result = lookup(domain, record_types=('MX', 'A', 'AAAA', 'TXT'))
    mx = result['records'].get('MX', {})
    values = mx.get('values', [])
    if '0 .' in values:
        mail = 'Domain explicitly does not accept email (Null MX).'
    elif values:
        mail = 'Mail servers advertised; mailbox existence is not verified.'
    elif mx.get('status') == 'no_records':
        mail = 'No MX record; A/AAAA fallback may apply. Mailbox existence is not verified.'
    else:
        mail = 'Mail configuration could not be established.'
    return {'email': email, 'mail_assessment': mail, 'dns': result,
            'note': 'Syntax and domain checks do not prove ownership or mailbox deliverability.'}
