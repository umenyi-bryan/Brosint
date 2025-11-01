def collect(username):
    return [
        {"source": "Sherlock", "type": "profile_found", "platform": "github", "url": f"https://github.com/{username}"},
        {"source": "Sherlock", "type": "not_found", "platform": "twitter"}
    ]
