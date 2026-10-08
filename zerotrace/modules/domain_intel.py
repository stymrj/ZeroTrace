"""DNS, Nameserver, and Security Records Inspection."""
import dns.resolver

def scan_domain(domain_input: str) -> dict:
    """Queries DNS records for domain reconnaissance."""
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

    return {
        "Domain": clean_domain,
        "A (IPv4 Addresses)": ", ".join(records.get("A", [])) or "None detected",
        "AAAA (IPv6 Addresses)": ", ".join(records.get("AAAA", [])) or "None detected",
        "Mail Servers (MX)": ", ".join(records.get("MX", [])) or "None detected",
        "Nameservers (NS)": ", ".join(records.get("NS", [])) or "None detected",
        "Security / TXT Records": " | ".join(records.get("TXT", [])[:3]) or "None detected",
    }
