def collect(email):
    return [
        {"source": "Hunter", "type": "enrichment", "data": {"email": email, "score": 0.91}},
        {"source": "HIBP", "type": "breach", "data": {"breach": "ExampleLeak2024"}}
    ]
