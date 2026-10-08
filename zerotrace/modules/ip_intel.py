"""Target IP and ASN Intelligence Gathering."""
import requests
from zerotrace.core.config import USER_AGENT, DEFAULT_TIMEOUT

def scan_ip(target_ip: str) -> dict:
    """Retrieves deep geolocation and network telemetry for an IP."""
    target_ip = target_ip.strip()
    url = f"http://ipwho.is/{target_ip}"
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
        data = response.json()
        if not data.get("success", True) and "message" in data:
            return {"error": data.get("message")}

        lat = data.get("latitude")
        lon = data.get("longitude")
        maps_link = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else "N/A"

        return {
            "Target IP": data.get("ip", target_ip),
            "Type": data.get("type", "N/A"),
            "Country": f"{data.get('country', 'N/A')} {data.get('flag', {}).get('emoji', '')}".strip(),
            "Country Code": data.get("country_code", "N/A"),
            "Region": data.get("region", "N/A"),
            "City": data.get("city", "N/A"),
            "Postal Code": data.get("postal", "N/A"),
            "Coordinates": f"{lat}, {lon}" if lat and lon else "N/A",
            "Google Maps": maps_link,
            "Autonomous System (ASN)": data.get("connection", {}).get("asn", "N/A"),
            "ISP / Organization": data.get("connection", {}).get("isp", "N/A"),
            "Domain": data.get("connection", {}).get("domain", "N/A"),
            "Timezone": data.get("timezone", {}).get("id", "N/A"),
            "Current Local Time": data.get("timezone", {}).get("current_time", "N/A"),
        }
    except Exception as e:
        return {"error": f"Failed to retrieve IP intelligence: {str(e)}"}

def get_my_ip() -> dict:
    """Resolves and scans caller's public IP."""
    try:
        resp = requests.get("https://api.ipify.org?format=json", timeout=DEFAULT_TIMEOUT)
        ip = resp.json().get("ip")
        return scan_ip(ip)
    except Exception as e:
        return {"error": f"Failed to resolve public IP: {str(e)}"}
