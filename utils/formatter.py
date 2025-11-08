# utils/formatter.py
import json
from datetime import datetime

def format_for_web(results):
    """
    Prepare a structured object for the dashboard.
    Keep values JSON-serializable.
    """
    out = {}
    for k, v in results.items():
        out[k] = v
    out["_generated_at"] = datetime.utcnow().isoformat() + "Z"
    return out

def to_pretty_json(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False)
