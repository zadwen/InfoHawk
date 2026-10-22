import phonenumbers
from phonenumbers import carrier, geocoder, timezone


def analyze(value, region='OM'):
    region = region.strip().upper()
    if region not in phonenumbers.SUPPORTED_REGIONS:
        raise ValueError('Use a two-letter country code such as OM, US or GB.')
    if len(value) > 100:
        raise ValueError('Phone number is too long.')
    try:
        number = phonenumbers.parse(value.strip(), region)
    except phonenumbers.NumberParseException as exc:
        raise ValueError('Enter a phone number, preferably with its +country code.') from exc
    valid = phonenumbers.is_valid_number(number)
    return {
        'international': phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
        'e164': phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164),
        'possible': phonenumbers.is_possible_number(number), 'valid_pattern': valid,
        'region': phonenumbers.region_code_for_number(number),
        'numbering_area': geocoder.description_for_number(number, 'en') if valid else '',
        'original_carrier': carrier.name_for_number(number, 'en') if valid else '',
        'time_zones': list(timezone.time_zones_for_number(number)) if valid else [],
        'source': 'Offline libphonenumber metadata',
        'note': 'Numbering-plan metadata only: not owner identity, active status or live location. Porting can change the carrier.'
    }
