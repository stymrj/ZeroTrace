"""Advanced Phone Number OSINT with Carrier, Fraud Heuristics & OSINT Dorks."""
import urllib.parse

try:
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone
    PHONENUMBERS_AVAILABLE = True
except ImportError:
    PHONENUMBERS_AVAILABLE = False

def scan_phone(phone_input: str, default_region: str = "US") -> dict:
    if not PHONENUMBERS_AVAILABLE:
        return {"error": "The 'phonenumbers' library is required. Install via: pip install phonenumbers"}

    phone_input = phone_input.strip()
    try:
        parsed = phonenumbers.parse(phone_input, default_region)
        if not phonenumbers.is_valid_number(parsed):
            return {"error": f"The number '{phone_input}' is invalid under international E.164 specifications."}

        num_type = phonenumbers.number_type(parsed)
        type_mapping = {
            phonenumbers.PhoneNumberType.MOBILE: "Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line (Landline)",
            phonenumbers.PhoneNumberType.VOIP: "VoIP (Virtual Number - High Fraud Risk)",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Toll-Free",
        }
        classified_type = type_mapping.get(num_type, "Other / Unknown")

        tz = timezone.time_zones_for_number(parsed)
        provider = carrier.name_for_number(parsed, "en") or "Not Identified / Private"
        location = geocoder.description_for_number(parsed, "en") or "Not Identified"

        e164_formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        international_formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        national_formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
        clean_digits = "".join(filter(str.isdigit, e164_formatted))

        dork_query = f'"{e164_formatted}" OR "{international_formatted}"'
        dork_url = f"https://www.google.com/search?q={urllib.parse.quote(dork_query)}"

        return {
            "Input Number": phone_input,
            "Validation Status": "Valid (E.164 Compliant)",
            "International Format": international_formatted,
            "National Format": national_formatted,
            "Country Code": f"+{parsed.country_code}",
            "Geographic Location": location,
            "Carrier": provider,
            "Line Classification": classified_type,
            "VoIP / Burner Risk": "HIGH (Virtual Number)" if "VoIP" in classified_type else "LOW (Standard Line)",
            "WhatsApp Deep Link": f"https://wa.me/{clean_digits}",
            "Google Leak Dork": dork_url,
            "Truecaller Web Search": f"https://www.truecaller.com/search/none/{clean_digits}",
        }
    except Exception as e:
        return {"error": f"Phone validation failed: {str(e)}"}
