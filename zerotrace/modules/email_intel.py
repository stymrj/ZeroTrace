"""Email address validation, MX check, and Gravatar lookup."""
import hashlib
import re
import dns.resolver
import requests
from zerotrace.core.config import DEFAULT_TIMEOUT

DISPOSABLE_DOMAINS = {
    "tempmail.com", "guerrillamail.com", "10minutemail.com", "mailinator.com",
    "sharklasers.com", "dispostable.com", "yopmail.com", "trashmail.com"
}

def scan_email(email_input: str) -> dict:
    """Audits email syntax, MX availability, disposable flag, and Gravatar presence."""
    email_clean = email_input.strip().lower()
    regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(regex, email_clean):
        return {"error": f"Invalid email format: '{email_input}'"}

    domain = email_clean.split("@")[-1]
    is_disposable = domain in DISPOSABLE_DOMAINS

    # MX check
    mx_found = False
    try:
        answers = dns.resolver.resolve(domain, "MX", lifetime=4.0)
        mx_records = [r.to_text() for r in answers]
        mx_found = len(mx_records) > 0
        mx_display = ", ".join(mx_records[:2])
    except Exception:
        mx_display = "No MX records found"

    # Gravatar check
    email_hash = hashlib.md5(email_clean.encode("utf-8")).hexdigest()
    gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"
    gravatar_found = False
    try:
        res = requests.head(gravatar_url, timeout=DEFAULT_TIMEOUT)
        gravatar_found = (res.status_code == 200)
    except Exception:
        pass

    return {
        "Email": email_clean,
        "Domain": domain,
        "Syntax Valid": "Yes",
        "Disposable Domain": "Yes (Burner / Temp)" if is_disposable else "No (Legitimate)",
        "MX Delivery Available": "Yes" if mx_found else "No (Cannot receive mail)",
        "Primary MX Servers": mx_display,
        "Gravatar Profile Exists": "Yes" if gravatar_found else "Not Found",
        "Gravatar Avatar URL": gravatar_url if gravatar_found else "N/A"
    }
