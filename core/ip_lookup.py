"""
Free-mode IP lookup using ip-api.com (no key). Limited rate but free.
"""
import requests

IPAPI_URL = "http://ip-api.com/json/"

def offline_ip_lookup(ip):
    return {"ip": ip, "city": None, "region": None, "country": None, "asn": None, "org": None}

def online_ip_lookup(ip):
    try:
        r = requests.get(IPAPI_URL + ip, timeout=6)
        if r.ok:
            return r.json()
        return {"error": f"status={r.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def lookup(ip, online=False):
    if online:
        return online_ip_lookup(ip)
    return offline_ip_lookup(ip)
