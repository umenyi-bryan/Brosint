"""
Free-mode social lookup: existence checks for common profile URLs.
Performs HEAD requests (lightweight).
"""
import requests

PLATFORMS = {
    "github":"https://github.com/{u}",
    "twitter":"https://twitter.com/{u}",
    "instagram":"https://www.instagram.com/{u}/",
    "linkedin":"https://www.linkedin.com/in/{u}/",
    "reddit":"https://www.reddit.com/user/{u}"
}

def offline_social_lookup(username):
    if not username: return {"matched_profiles":[]}
    if username.lower() in ("janedoe","chinedu"):
        return {"matched_profiles":[{"platform":"github","url":f"https://github.com/{username}"}]}
    return {"matched_profiles":[]}

def online_social_lookup(username):
    if not username:
        return {"matched_profiles":[]}
    found = []
    headers = {"User-Agent":"BROsint-Free/1.0"}
    for name, tpl in PLATFORMS.items():
        url = tpl.format(u=username)
        try:
            r = requests.head(url, headers=headers, timeout=6, allow_redirects=True)
            if r.status_code == 200:
                found.append({"platform": name, "url": url})
        except Exception:
            # ignore network errors and timeouts
            pass
    return {"matched_profiles": found}

def lookup(username, online=False):
    if online:
        return online_social_lookup(username)
    return offline_social_lookup(username)
