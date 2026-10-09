"""Advanced IP, ASN, Threat, and Shodan InternetDB Intelligence."""
import socket
import requests
from zerotrace.core.config import USER_AGENT, DEFAULT_TIMEOUT

def scan_ip(target_ip: str) -> dict:
    target_ip = target_ip.strip()
    headers = {"User-Agent": USER_AGENT}
    results = {}

    try:
        r = requests.get(f"http://ipwho.is/{target_ip}", headers=headers, timeout=DEFAULT_TIMEOUT)
        data = r.json()
        if not data.get("success", True) and "message" in data:
            return {"error": data.get("message")}

        lat = data.get("latitude")
        lon = data.get("longitude")
        results["Target IP"] = data.get("ip", target_ip)
        results["IP Version"] = data.get("type", "IPv4")
        results["Country"] = f"{data.get('country', 'N/A')} {data.get('flag', {}).get('emoji', '')}".strip()
        results["Region / City"] = f"{data.get('region', 'N/A')}, {data.get('city', 'N/A')} ({data.get('postal', 'N/A')})"
        results["Coordinates"] = f"{lat}, {lon}" if lat and lon else "N/A"
        results["Google Maps"] = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else "N/A"
        results["ASN"] = data.get("connection", {}).get("asn", "N/A")
        results["ISP / Organization"] = data.get("connection", {}).get("isp", "N/A")
        results["Organization Org"] = data.get("connection", {}).get("org", "N/A")
        results["Timezone"] = f"{data.get('timezone', {}).get('id', 'N/A')} (UTC {data.get('timezone', {}).get('utc', 'N/A')})"
        results["Local Time"] = data.get("timezone", {}).get("current_time", "N/A")
    except Exception as e:
        return {"error": f"Failed to fetch IP geolocation: {str(e)}"}

    try:
        hostname, _, _ = socket.gethostbyaddr(target_ip)
        results["Reverse DNS (PTR)"] = hostname
    except Exception:
        results["Reverse DNS (PTR)"] = "None (No PTR record)"

    try:
        shodan_res = requests.get(f"https://internetdb.shodan.io/{target_ip}", headers=headers, timeout=5)
        if shodan_res.status_code == 200:
            sdata = shodan_res.json()
            ports = sdata.get("ports", [])
            vulns = sdata.get("vulns", [])
            results["Shodan Open Ports"] = ", ".join(map(str, ports)) if ports else "None detected (Firewalled)"
            results["Known Vulnerabilities (CVEs)"] = ", ".join(vulns) if vulns else "None publicly indexed"
        else:
            results["Shodan Open Ports"] = "None detected (Firewalled)"
            results["Known Vulnerabilities (CVEs)"] = "Clean / None indexed"
    except Exception:
        results["Shodan Open Ports"] = "Lookup timed out"

    isp_lower = str(results.get("ISP / Organization", "")).lower()
    org_lower = str(results.get("Organization Org", "")).lower()
    datacenter_keywords = ["amazon", "aws", "google", "cloud", "digitalocean", "linode", "ovh", "microsoft", "azure", "hetzner", "vultr", "cloudflare"]
    is_hosting = any(kw in isp_lower or kw in org_lower for kw in datacenter_keywords)
    results["Classification"] = "Hosting / Cloud / Datacenter (VPN/Proxy likely)" if is_hosting else "Residential / Broadband"

    return results

def get_my_ip() -> dict:
    try:
        resp = requests.get("https://api.ipify.org?format=json", timeout=DEFAULT_TIMEOUT)
        ip = resp.json().get("ip")
        return scan_ip(ip)
    except Exception as e:
        return {"error": f"Failed to resolve public IP: {str(e)}"}
