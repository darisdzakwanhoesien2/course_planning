import json
from pathlib import Path

BASE_DATA = Path("data")

def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_minors():
    minor_dir = BASE_DATA / "minors"
    return sorted(minor_dir.glob("*.json"))

def load_minor(minor_id: str):
    path = BASE_DATA / "minors" / f"{minor_id}.json"
    return load_json(path)

def load_course(course_id: str):
    path = BASE_DATA / "courses" / f"{course_id}.json"
    return load_json(path)
