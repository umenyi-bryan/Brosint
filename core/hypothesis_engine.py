"""
Improved hypothesis engine that reasons over structured results.
Returns an explainable hypothesis dict.
"""
from datetime import datetime

def generate_hypothesis(structured):
    reasons = []
    results = structured.get("results", {})

    # Email signals
    em = results.get("email_intel") or {}
    if em.get("breaches"):
        reasons.append("Email found in public breach(s).")
    if em.get("enrichment") and isinstance(em.get("enrichment"), dict):
        reasons.append("Email verification/enrichment data available.")

    # Social signals
    soc = results.get("social_intel") or {}
    matches = soc.get("matched_profiles") or []
    if matches:
        reasons.append(f"{len(matches)} social profile(s) found: " + ", ".join([p.get("platform") for p in matches if p.get("platform")]))

    # Whois signals
    who = results.get("whois") or {}
    if isinstance(who, dict) and who.get("domain"):
        reasons.append("Domain WHOIS data present.")

    # IP signals
    ip = results.get("ip_intel") or {}
    if ip.get("country"):
        reasons.append(f"IP geolocation: {ip.get('country')}")

    # Meta signals
    meta = results.get("meta") or {}
    if meta.get("exif"):
        reasons.append("File EXIF metadata extracted.")

    # Score
    score = 0
    for r in reasons:
        if "breach" in r.lower(): score += 30
        if "social" in r.lower(): score += 20
        if "whois" in r.lower(): score += 10
        if "ip geolocation" in r.lower(): score += 5
        if "exif" in r.lower(): score += 5

    confidence = max(0, min(100, score))
    level = "low"
    if confidence >= 75:
        level = "high"
    elif confidence >= 40:
        level = "medium"

    summary = "; ".join(reasons) if reasons else "Insufficient public signals."

    return {
        "hypothesis": summary,
        "confidence": confidence,
        "level": level,
        "reasons": reasons,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
