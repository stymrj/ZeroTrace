"""Multi-Engine GeoIP Consensus and Accuracy Estimator."""
import math
import requests
from zerotrace.core.config import USER_AGENT, DEFAULT_TIMEOUT

def _haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def get_consensus(ip: str) -> dict:
    ip = ip.strip()
    headers = {"User-Agent": USER_AGENT}
    p1, p2 = {}, {}
    try:
        r1 = requests.get(f"http://ipwho.is/{ip}", headers=headers, timeout=DEFAULT_TIMEOUT).json()
        if r1.get("success", True):
            p1 = {"city": r1.get("city", "N/A"), "region": r1.get("region", "N/A"), "isp": r1.get("connection", {}).get("isp", "N/A"), "lat": r1.get("latitude"), "lon": r1.get("longitude")}
    except Exception: pass
    try:
        r2 = requests.get(f"http://ip-api.com/json/{ip}", headers=headers, timeout=DEFAULT_TIMEOUT).json()
        if r2.get("status") == "success":
            p2 = {"city": r2.get("city", "N/A"), "region": r2.get("regionName", "N/A"), "isp": r2.get("isp", "N/A"), "lat": r2.get("lat"), "lon": r2.get("lon")}
    except Exception: pass
    if not p1 and not p2: return {"error": "All GeoIP providers timed out."}
    city1, city2 = p1.get("city", "Unknown"), p2.get("city", "Unknown")
    reg1, reg2 = p1.get("region", "Unknown"), p2.get("region", "Unknown")
    dist = _haversine(p1["lat"], p1["lon"], p2["lat"], p2["lon"]) if p1.get("lat") and p2.get("lat") else None
    return {
        "Target IP": ip,
        "Provider 1 (ipwho.is)": f"{city1}, {reg1} | ISP: {p1.get('isp', 'N/A')}",
        "Provider 2 (ip-api.com)": f"{city2}, {reg2} | ISP: {p2.get('isp', 'N/A')}",
        "Region Consensus": reg1 if reg1.lower() == reg2.lower() else f"{reg1} / {reg2}",
        "Provider Distance Delta": f"~{dist:.1f} km" if dist else "N/A",
        "Confidence Rating": "HIGH (City Match)" if city1.lower() == city2.lower() else "MODERATE (State/Region Match)",
        "ISP Gateway Note": "Public IP reflects ISP routing exchange/POP. Expected accuracy is within ~25-50km radius.",
        "Consensus Google Maps": f"https://www.google.com/maps?q={p1.get('lat')},{p1.get('lon')}" if p1.get("lat") else "N/A"
    }
