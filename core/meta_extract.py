import os
try:
    import exifread
except Exception:
    exifread = None
from utils.cache import load, save

def offline_meta(path):
    return {"filename": os.path.basename(path), "exif": None}

def online_meta(path):
    key = f"meta:{path}"
    cached = load(key)
    if cached: return cached
    if not exifread:
        out = {"error":"exifread not installed"}
        save(key, out, ttl=600)
        return out
    try:
        with open(path,'rb') as f:
            tags = exifread.process_file(f, details=False)
            data = {k: str(tags[k]) for k in tags}
            save(key, {"filename": os.path.basename(path), "exif": data}, ttl=3600)
            return {"filename": os.path.basename(path), "exif": data}
    except Exception as e:
        out = {"error": str(e)}
        save(key, out, ttl=300)
        return out

def extract(path, online=False):
    if online:
        return online_meta(path)
    return offline_meta(path)
