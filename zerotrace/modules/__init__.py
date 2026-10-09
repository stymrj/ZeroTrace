"""ZeroTrace Reconnaissance Modules."""
import sys, os, importlib.util
_dir = os.path.dirname(__file__)
for _mod in ["exif_intel", "url_intel", "geoip_consensus", "mac_intel", "ip_intel", "phone_intel", "username_intel", "domain_intel", "email_intel"]:
    _path = os.path.join(_dir, f"{_mod}.py")
    if os.path.exists(_path) and f"zerotrace.modules.{_mod}" not in sys.modules:
        _spec = importlib.util.spec_from_file_location(f"zerotrace.modules.{_mod}", _path)
        if _spec and _spec.loader:
            _m = importlib.util.module_from_spec(_spec)
            sys.modules[f"zerotrace.modules.{_mod}"] = _m
            _spec.loader.exec_module(_m)
