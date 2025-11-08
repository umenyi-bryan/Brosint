# core/email_lookup.py
import dns.resolver
import hashlib
import requests

def mx_lookup(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX', lifetime=8)
        return [str(r.exchange).rstrip('.') for r in answers]
    except Exception:
        return []

def has_gravatar(email):
    try:
        h = hashlib.md5(email.strip().lower().encode()).hexdigest()
        url = f"https://www.gravatar.com/avatar/{h}?d=404"
        r = requests.get(url, timeout=6)
        return r.status_code == 200
    except Exception:
        return False

def lookup(email):
    out = {"email": email}
    try:
        if "@" in email:
            domain = email.split("@",1)[1]
        else:
            domain = ""
    except Exception:
        domain = ""
    out["domain"] = domain
    out["mx"] = mx_lookup(domain) if domain else []
    out["gravatar"] = has_gravatar(email)
    return out
