"""Social media username footprinting with async engine and sync fallback."""
import asyncio
from zerotrace.core.config import USER_AGENT, DEFAULT_TIMEOUT, SOCIAL_TARGETS

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

async def _check_site_aiohttp(session, site: dict, username: str) -> dict:
    url = site["url"].format(username)
    check_type = site.get("check", "status_200")
    try:
        async with session.get(url, timeout=DEFAULT_TIMEOUT, allow_redirects=True) as resp:
            found = False
            if check_type == "status_200" and resp.status == 200:
                found = True
            elif check_type == "json_data" and resp.status == 200:
                try:
                    data = await resp.json()
                    if isinstance(data, dict) and ("data" in data or "name" in data or "id" in data):
                        found = True
                except Exception:
                    found = False

            return {"name": site["name"], "url": url, "found": found, "status": resp.status}
    except Exception:
        return {"name": site["name"], "url": url, "found": False, "status": "Timeout/Error"}

def _check_site_requests(site: dict, username: str) -> dict:
    url = site["url"].format(username)
    headers = {"User-Agent": USER_AGENT}
    try:
        resp = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT, allow_redirects=True)
        found = (resp.status_code == 200)
        return {"name": site["name"], "url": url, "found": found, "status": resp.status_code}
    except Exception:
        return {"name": site["name"], "url": url, "found": False, "status": "Timeout/Error"}

async def scan_username(username: str) -> list:
    """Audits social targets for presence of username."""
    if AIOHTTP_AVAILABLE:
        headers = {"User-Agent": USER_AGENT}
        connector = aiohttp.TCPConnector(ssl=False, limit=20)
        async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
            tasks = [_check_site_aiohttp(session, site, username) for site in SOCIAL_TARGETS]
            results = await asyncio.gather(*tasks, return_exceptions=False)
            return results
    else:
        # Fallback to concurrent thread pool with requests
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(None, _check_site_requests, site, username) for site in SOCIAL_TARGETS]
        results = await asyncio.gather(*tasks)
        return results
