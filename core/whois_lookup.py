"""
Whois lookup: wraps python-whois with caching.
"""
import whois
from utils.cache import load, save

def offline_whois(domain):
    return {"domain": domain, "owner": "demo_owner", "created": "2020-01-01"}

def online_whois(domain):
    key = f"whois:{domain}"
    c = load(key)
    if c: return c
    try:
        w = whois.whois(domain)
        out = dict(w)
    except Exception as e:
        out = {"error": str(e)}
    save(key,out,ttl=86400); return out

def lookup(domain, online=False):
    if online:
        return online_whois(domain)
    return offline_whois(domain)
