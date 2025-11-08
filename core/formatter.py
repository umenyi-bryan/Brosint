import json

def prettify(title, data):
    return f"\n{'='*10} {title} {'='*10}\n{json.dumps(data, indent=2)}\n"
