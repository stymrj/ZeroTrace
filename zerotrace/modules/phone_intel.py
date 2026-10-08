"""Phone Number OSINT using Google libphonenumber."""
try:
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone
    PHONENUMBERS_AVAILABLE = True
except ImportError:
    PHONENUMBERS_AVAILABLE = False

def scan_phone(phone_input: str, default_region: str = "US") -> dict:
    """Parses and enriches an international phone number."""
    if not PHONENUMBERS_AVAILABLE:
        return {
            "error": "The 'phonenumbers' library is required for phone intelligence. Run: pip install phonenumbers"
        }

    phone_input = phone_input.strip()
    try:
        parsed = phonenumbers.parse(phone_input, default_region)
        if not phonenumbers.is_valid_number(parsed):
            return {"error": f"The number '{phone_input}' is invalid under international E.164 specifications."}

        num_type = phonenumbers.number_type(parsed)
        type_mapping = {
            phonenumbers.PhoneNumberType.MOBILE: "Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line (Landline)",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line / Mobile",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Toll-Free",
            phonenumbers.PhoneNumberType.VOIP: "VoIP (Virtual Number)",
            phonenumbers.PhoneNumberType.PAGER: "Pager",
            phonenumbers.PhoneNumberType.UAN: "Universal Access Number (UAN)",
            phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
        }
        classified_type = type_mapping.get(num_type, "Other / Unknown")

        tz = timezone.time_zones_for_number(parsed)
        provider = carrier.name_for_number(parsed, "en") or "Not Identified / Private"
        location = geocoder.description_for_number(parsed, "en") or "Not Identified"

        e164_formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        international_formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        national_formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)

        clean_digits = "".join(filter(str.isdigit, e164_formatted))

        return {
            "Input Number": phone_input,
            "Valid": "True (E.164 compliant)",
            "International": international_formatted,
            "National Format": national_formatted,
            "E.164 Format": e164_formatted,
            "Country Code": f"+{parsed.country_code}",
            "Geographic Location": location,
            "Carrier / Provider": provider,
            "Line Classification": classified_type,
            "Timezone(s)": ", ".join(tz) if tz else "N/A",
            "WhatsApp Chat Link": f"https://wa.me/{clean_digits}",
        }
    except Exception as e:
        return {"error": f"Phone validation failed: {str(e)}"}
