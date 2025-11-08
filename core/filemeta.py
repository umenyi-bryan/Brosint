# core/filemeta.py
from PIL import Image
from PIL.ExifTags import TAGS
import os

def extract(path):
    out = {"filename": os.path.basename(path), "exif": {}}
    try:
        img = Image.open(path)
        exif = img._getexif() or {}
        for k, v in exif.items():
            name = TAGS.get(k, k)
            try:
                out["exif"][name] = str(v)
            except Exception:
                out["exif"][name] = repr(v)
    except Exception as e:
        out["error"] = str(e)
    return out
