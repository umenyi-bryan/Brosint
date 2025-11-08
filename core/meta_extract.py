def extract(file_path: str) -> dict:
    """Mock metadata extraction"""
    return {
        "filename": file_path.split("/")[-1],
        "exif": None
    }
