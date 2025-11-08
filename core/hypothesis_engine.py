# core/hypothesis_engine.py
from datetime import datetime

def analyze(results):
    reasons = []
    if results.get("email"):
        e = results["email"]
        if e.get("gravatar"):
            reasons.append("Email has a Gravatar — likely publicly used for avatars.")
        if e.get("mx"):
            reasons.append("Email domain has MX records.")
    if results.get("social") and results["social"].get("matched_profiles"):
        reasons.append(f"Found {len(results['social']['matched_profiles'])} public social profile(s).")
    if results.get("whois") and results["whois"].get("registrar"):
        reasons.append("WHOIS registrar data found for domain.")
    if results.get("filemeta") and results["filemeta"].get("exif"):
        if results["filemeta"]["exif"]:
            reasons.append("Image file contains EXIF metadata.")

    score = min(100, 20 * len(reasons))
    level = "low"
    if score >= 75:
        level = "high"
    elif score >= 40:
        level = "medium"

    return {
        "hypothesis": "; ".join(reasons) if reasons else "No strong public signals.",
        "confidence": score,
        "level": level,
        "reasons": reasons,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
