"""
Free-mode email lookup (no API keys).
- MX record check via dnspython
- Gravatar check (public)
- Basic domain resolution
"""
import hashlib, socket, requests
import dns.resolver

def _mx_lookup(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX', lifetime=6)
        mx = [str(r.exchange).rstrip('.') for r in answers]
        return {"mx": mx}
    except Exception as e:
        return {"mx_error": str(e)}

def _domain_resolves(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

def _gravatar_exists(email):
    try:
        e = email.strip().lower().encode('utf-8')
        h = hashlib.md5(e).hexdigest()
        url = f"https://www.gravatar.com/avatar/{h}?d=404"
        r = requests.get(url, timeout=6)
        return r.status_code == 200, url
    except Exception:
        return False, None

def offline_email_lookup(email):
    domain = email.split('@')[-1] if '@' in email else None
    return {"email": email, "domain": domain, "mx": None, "domain_resolves": False, "gravatar": False}

def online_email_lookup(email):
    domain = email.split('@')[-1] if '@' in email else None
    result = {"email": email, "domain": domain}
    if domain:
        result.update(_mx_lookup(domain))
        result["domain_resolves"] = _domain_resolves(domain)
    exists, grav_url = _gravatar_exists(email)
    result["gravatar"] = {"exists": exists, "url": grav_url}
    return result

def lookup(email, online=False):
    if online:
        return online_email_lookup(email)
    return offline_email_lookup(email)
