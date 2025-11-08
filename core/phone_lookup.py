"""
Phone lookup: normalizes numbers (phonenumbers), optional online via Numverify/AbstractAPI.
"""
import os, requests
from utils.cache import load, save
import phonenumbers

NUMVERIFY_KEY = os.getenv("NUMVERIFY_KEY")
ABSTRACT_KEY = os.getenv("ABSTRACTAPI_PHONE_KEY")

def offline_phone_lookup(phone):
    try:
        p = phonenumbers.parse(phone, None)
        e164 = phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)
        region = phonenumbers.region_code_for_number(p)
    except Exception:
        e164 = phone
        region = None
    return {"number": e164, "region": region, "carrier": None, "type": "mobile"}

def online_phone_lookup(phone):
    key = f"phone:{phone}"
    cached = load(key)
    if cached: return cached
    if NUMVERIFY_KEY:
        try:
            r = requests.get("http://apilayer.net/api/validate", params={"access_key": NUMVERIFY_KEY, "number": phone}, timeout=10)
            out = r.json() if r.ok else {"error": f"numverify status {r.status_code}"}
            save(key, out, ttl=3600)
            return out
        except Exception as e:
            out = {"error": str(e)}
            save(key, out, ttl=300)
            return out
    if ABSTRACT_KEY:
        try:
            r = requests.get("https://phonevalidation.abstractapi.com/v1/?api_key="+ABSTRACT_KEY+"&phone="+phone, timeout=10)
            out = r.json() if r.ok else {"error": f"abstract status {r.status_code}"}
            save(key, out, ttl=3600)
            return out
        except Exception as e:
            out = {"error": str(e)}
            save(key, out, ttl=300)
            return out
    out = {"note":"No phone API key set", "data": offline_phone_lookup(phone)}
    save(key, out, ttl=600)
    return out

def lookup(phone, online=False):
    if online:
        return online_phone_lookup(phone)
    return offline_phone_lookup(phone)
