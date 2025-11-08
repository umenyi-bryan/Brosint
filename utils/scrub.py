import re, json, os

EMAIL_RE = re.compile(r'([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')
PHONE_RE = re.compile(r'(\+?\d[\d\-\s]{4,}\d)')
URL_RE = re.compile(r'https?://[^\s"\']+')

def _redact_email(m):
    user = m.group(1)
    domain = m.group(2)
    return f"{user[0]}***@{domain.split('.')[0]}***"

def scrub_obj(obj):
    s = json.dumps(obj)
    s = EMAIL_RE.sub(_redact_email, s)
    s = PHONE_RE.sub("[REDACTED_PHONE]", s)
    s = URL_RE.sub("[REDACTED_URL]", s)
    return json.loads(s)

def scrub_file(input_path, output_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(input_path)
    with open(input_path, "r") as f:
        data = json.load(f)
    redacted = scrub_obj(data)
    with open(output_path, "w") as o:
        json.dump(redacted, o, indent=2)
    return output_path
