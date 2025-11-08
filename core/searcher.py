# core/searcher.py
import requests
from urllib.parse import quote_plus

DDG_INSTANT_URL = "https://api.duckduckgo.com/"

def search(query, limit=10):
    """
    Free search wrapper — uses DuckDuckGo Instant Answer API as fallback.
    Returns list of dicts: {title, link, snippet}
    """
    q = query.strip()
    results = []
    try:
        params = {"q": q, "format": "json", "no_redirect": 1, "no_html": 1}
        r = requests.get(DDG_INSTANT_URL, params=params, timeout=10)
        j = r.json()
        # abstract
        abstract = j.get("AbstractText")
        if abstract:
            results.append({"title": "Summary", "link": "", "snippet": abstract})
        # RelatedTopics may contain entries
        rt = j.get("RelatedTopics", [])
        for item in rt:
            if isinstance(item, dict):
                text = item.get("Text") or ""
                first = item.get("FirstURL") or ""
                results.append({"title": text[:80], "link": first, "snippet": text})
            elif isinstance(item, list):
                for it in item[:limit]:
                    results.append({"title": it.get("Text")[:80], "link": it.get("FirstURL"), "snippet": it.get("Text")})
        # Trim
        return results[:limit]
    except Exception:
        return []
