import json
from pathlib import Path

# За замовчуванням — 1280×720
_DEFAULT = {
    "resolution": [1280, 720],
    "difficulty": "normal",   # normal / hard
    "sound": True,
    "high_score": 0
}
_FILE = Path("settings.json")

def load_settings():
    if _FILE.exists():
        with open(_FILE, "r", encoding="utf-8") as f:
            _DEFAULT.update(json.load(f))
    # повертаємо копію, щоб оригінал не змінювався випадково
    return _DEFAULT.copy()

def save_settings(data):
    with open(_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)