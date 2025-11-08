# core/social_lookup.py
from .searcher import search

COMMON_SITES = ["github.com", "twitter.com", "linkedin.com", "instagram.com", "facebook.com"]

def lookup(username, limit=10):
    results = {"matched_profiles": []}
    if not username:
        return results
    q = f'"{username}"'
    hits = search(q, limit=limit)
    for h in hits:
        url = (h.get("link") or "").lower()
        title = h.get("title") or ""
        if any(site in url for site in COMMON_SITES) or username.lower() in title.lower() or username.lower() in (h.get("snippet") or "").lower():
            # Try to assign platform based on URL heuristics
            platform = None
            for s in COMMON_SITES:
                if s in url:
                    platform = s.split(".")[0]
                    break
            results["matched_profiles"].append({"platform": platform, "url": h.get("link"), "title": title})
    return results

