"""Resolve cached translations; fail instead of silently emitting French."""
import json
from pathlib import Path

CACHE = Path(__file__).resolve().parents[1] / "data/translations-en.json"
_cache = None
OVERRIDES = {
    "Développeur / Développeuse informatique": "Software Developer",
    "Assistant social / Assistante sociale": "Social Worker",
    "Responsable qualité en industrie": "Industrial Quality Manager",
    "Administrateur / Administratrice réseaux - télécoms": "Network and Telecommunications Administrator",
    "Administrateur / Administratrice de systèmes d'information (SI)": "Information Systems Administrator",
    "Médecin généraliste": "General Practitioner",
}


def tr(text):
    global _cache
    if text in OVERRIDES:
        return OVERRIDES[text]
    if _cache is None:
        _cache = json.loads(CACHE.read_text(encoding="utf-8"))
    if not text:
        return text
    value = _cache[text]
    parts = [p.strip() for p in value.split(" / ")]
    if len(parts) > 1 and len({p.casefold() for p in parts}) == 1:
        return parts[0]
    return value
