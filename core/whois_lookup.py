# core/whois_lookup.py
import whois
import tldextract

def lookup(domain):
    out = {"domain": domain}
    try:
        w = whois.whois(domain)
        # convert possibly non-serializable fields to strings
        out.update({
            "registrar": w.registrar,
            "creation_date": str(w.creation_date) if w.creation_date else None,
            "expiration_date": str(w.expiration_date) if w.expiration_date else None,
            "name": w.name if hasattr(w, "name") else None
        })
    except Exception:
        ed = tldextract.extract(domain)
        out["registered"] = False
        out["domain_parsed"] = f"{ed.domain}.{ed.suffix}" if ed.suffix else ed.domain
    return out
