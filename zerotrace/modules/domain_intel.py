"""Advanced Domain, Subdomain Discovery (crt.sh), and DNS Intelligence."""
import requests
import dns.resolver
from zerotrace.core.config import USER_AGENT, DEFAULT_TIMEOUT

def scan_domain(domain_input: str) -> dict:
    clean_domain = domain_input.replace("https://", "").replace("http://", "").split("/")[0].strip()
    records = {}
    record_types = ["A", "AAAA", "MX", "NS", "TXT"]

    resolver = dns.resolver.Resolver()
    resolver.timeout = 4.0
    resolver.lifetime = 4.0

    for rtype in record_types:
        try:
            answers = resolver.resolve(clean_domain, rtype)
            records[rtype] = [r.to_text() for r in answers]
        except Exception:
            records[rtype] = []

    subdomains = set()
    try:
        headers = {"User-Agent": USER_AGENT}
        r = requests.get(f"https://crt.sh/?q=%.{clean_domain}&output=json", headers=headers, timeout=DEFAULT_TIMEOUT)
        if r.status_code == 200:
            for entry in r.json()[:25]:
                name_value = entry.get("name_value", "")
                for sub in name_value.split("\n"):
                    sub = sub.strip().lower()
                    if clean_domain in sub and not sub.startswith("*"):
                        subdomains.add(sub)
    except Exception:
        pass

    sub_list = sorted(list(subdomains))[:8]
    subdomain_str = ", ".join(sub_list) if sub_list else "None indexed in CT logs"

    return {
        "Target Domain": clean_domain,
        "A (IPv4 Addresses)": ", ".join(records.get("A", [])) or "None detected",
        "AAAA (IPv6 Addresses)": ", ".join(records.get("AAAA", [])) or "None detected",
        "Mail Servers (MX)": ", ".join(records.get("MX", [])) or "None detected",
        "Nameservers (NS)": ", ".join(records.get("NS", [])) or "None detected",
        "Indexed Subdomains (crt.sh)": subdomain_str,
        "Subdomain Count": str(len(subdomains)),
        "SSL Labs Test": f"https://www.ssllabs.com/ssltest/analyze.html?d={clean_domain}",
    }
