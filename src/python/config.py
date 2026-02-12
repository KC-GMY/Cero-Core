from pathlib import Path
import os,json
PROJECT_ROOT = Path(__file__).parent
ASSETS_DIR = PROJECT_ROOT / "Assets"
THEME_DIR = ASSETS_DIR / "Theme"
SETTINGS_PATH = ASSETS_DIR / "Settings.json"
ARDUINO_DIR = PROJECT_ROOT / "Arduino"
DB_PATH = PROJECT_ROOT / "database.db"

DEFAULT_SETTINGS = {
  "CTkTheme": "flipperzero.json",
  "CTkMode": "light",
  "CTkWindowsize": "160x128",
  "baudrate": 9600,
  "serial_ports": {
    "kHz": "COM7",
    "MHz": "COM7",
    "GHz": "COM9",
    "Ir": "COM9"
  }
}

def load_settings(path: str) -> dict:
    settings = DEFAULT_SETTINGS.copy()
    try:
        with open(path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            if isinstance(loaded, dict):
                settings.update({k: v for k, v in loaded.items() if k in DEFAULT_SETTINGS})
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        pass
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
    except OSError:
        pass
    return settings

def resolve_theme_path(theme_filename: str) -> str:
    candidate = os.path.join(THEME_DIR, theme_filename)
    if os.path.isfile(candidate):
        return candidate
    fallback = os.path.join(THEME_DIR, DEFAULT_SETTINGS["CTkTheme"])
    return fallback if os.path.isfile(fallback) else candidate