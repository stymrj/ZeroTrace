"""URL Unshortener, Redirect Hop Tracer, and Phishing Defanger."""
import urllib.parse
import requests
from zerotrace.core.config import USER_AGENT, DEFAULT_TIMEOUT

def defang_url(url: str) -> str:
    defanged = url.replace("http://", "hxxp[://]").replace("https://", "hxxps[://]")
    parts = defanged.split("/")
    if len(parts) > 2:
        parts[2] = parts[2].replace(".", "[.]")
        return "/".join(parts)
    return defanged.replace(".", "[.]")

def unshorten_url(target_url: str) -> dict:
    target_url = target_url.strip()
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url
    headers = {"User-Agent": USER_AGENT}
    try:
        session = requests.Session()
        resp = session.get(target_url, headers=headers, timeout=DEFAULT_TIMEOUT, allow_redirects=True)
        hops = [f"Hop {i}: [{h.status_code}] -> {h.url}" for i, h in enumerate(resp.history, start=1)]
        final_url = resp.url
        parsed = urllib.parse.urlparse(final_url)
        params = urllib.parse.parse_qs(parsed.query)
        param_str = ", ".join(f"{k}={v[0]}" for k, v in params.items()) if params else "None"
        return {
            "Original URL": target_url,
            "Final Destination URL": final_url,
            "Total Redirect Hops": str(len(resp.history)),
            "Redirect Chain": " | ".join(hops) if hops else "Direct link (No redirects)",
            "Final Domain": parsed.netloc,
            "Final Status Code": str(resp.status_code),
            "URL Parameters Tracked": param_str,
            "Defanged Safe URL": defang_url(final_url),
            "Redirection Alert": "Redirected (Shortened / Tracking link)" if len(resp.history) > 0 else "Clean / Direct URL"
        }
    except Exception as e:
        return {"error": f"Failed to trace URL: {str(e)}"}
