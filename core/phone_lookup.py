# core/phone_lookup.py
import phonenumbers

def lookup(number):
    try:
        p = phonenumbers.parse(number, None)
        info = {
            "raw": number,
            "international": phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "country": phonenumbers.region_code_for_number(p),
            "valid": phonenumbers.is_valid_number(p),
            "possible": phonenumbers.is_possible_number(p)
        }
    except Exception as e:
        info = {"error": "invalid format", "detail": str(e)}
    return info
