import json
from pathlib import Path

SETTINGS_PATH = Path(__file__).parent.parent / "settings.json"

def _load_settings():
    """Função interna para carregar as configurações do arquivo JSON."""
    with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

settings = _load_settings()