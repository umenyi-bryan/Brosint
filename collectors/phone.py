def collect(phone):
    return [
        {"source": "PhoneInfoga", "type": "scan", "data": {"number": phone, "region": "NG", "carrier": "MTN"}},
    ]
