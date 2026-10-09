"""MAC Address and Wi-Fi BSSID Hardware Vendor Lookup."""
import re
import requests
from zerotrace.core.config import USER_AGENT, DEFAULT_TIMEOUT

OUI_DATABASE = {
    "00:1A:2B": "Ayecom Technology", "00:0C:29": "VMware, Inc.", "00:50:56": "VMware, Inc.",
    "00:15:5D": "Microsoft Corporation", "B8:27:EB": "Raspberry Pi Foundation",
    "00:1E:C2": "Apple, Inc.", "3C:07:54": "Apple, Inc.", "18:FE:34": "Espressif Inc. (ESP8266/ESP32 IoT)",
    "00:26:86": "Cisco Systems", "00:14:D1": "TP-Link Technologies", "00:24:D7": "Intel Corporate",
    "00:23:D7": "Samsung Electronics", "70:4D:7B": "Xiaomi Communications", "00:1E:10": "Huawei Technologies",
}

def lookup_mac(mac_input: str) -> dict:
    clean_mac = re.sub(r"[^a-fA-F0-9]", "", mac_input.strip()).upper()
    if len(clean_mac) < 6: return {"error": "Invalid MAC address. Enter at least 6 hex characters."}
    oui_prefix = ":".join(clean_mac[i:i+2] for i in range(0, 6, 2))
    formatted_mac = ":".join(clean_mac[i:i+2] for i in range(0, min(12, len(clean_mac)), 2))
    vendor = OUI_DATABASE.get(oui_prefix)
    source = "Local Offline OUI Cache"
    if not vendor:
        try:
            r = requests.get(f"https://api.maclookup.app/v2/macs/{clean_mac[:6]}", headers={"User-Agent": USER_AGENT}, timeout=DEFAULT_TIMEOUT)
            if r.status_code == 200 and r.json().get("found"):
                vendor = r.json().get("company", "Unknown Vendor")
                source = "MacLookup Cloud Registry"
        except Exception: pass
    if not vendor: vendor = "Unknown / Unregistered Vendor"
    is_rand = (len(clean_mac) >= 2 and clean_mac[1].upper() in ("2", "6", "A", "E"))
    return {
        "Input MAC / BSSID": mac_input,
        "Normalized Format": formatted_mac,
        "Hardware Manufacturer": vendor,
        "Data Source": source,
        "Randomized MAC Check": "YES (Private Wi-Fi Address Active)" if is_rand else "NO (Burned-in Hardware MAC)",
        "Device Family Hint": "Virtual Machine" if "VMware" in vendor else ("IoT Microcontroller" if "Espressif" in vendor or "Raspberry" in vendor else "Standard Electronics")
    }
