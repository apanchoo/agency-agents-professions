"""Extrait textes paginés et fiches SAÉ/ressources des 24 PDF ministériels."""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
import unicodedata

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean(value):
    return re.sub(r"[ \t]+", " ", unicodedata.normalize("NFKC", value)).strip()


HEADER = re.compile(r"^\s*(?:(?:\d+\.)+\s*)?(?P<kind>SA[ÉE]|Ressource)\s+(?P<code>(?:R\s*)?\d[\w.\-]*\d)\s*:\s*(?P<title>.+)", re.I)


def extract(source):
    pdf = ROOT / source["pdf"]
    digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
    cached = ROOT / f"sources/but-text/{source['id']}.json"
    if cached.exists():
        result = json.loads(cached.read_text(encoding="utf-8"))
        if result.get("sha256") == digest:
            return result["programme"]
    reader = PdfReader(pdf)
    pages = [{"page": i + 1, "text": clean(page.extract_text() or "")} for i, page in enumerate(reader.pages)]
    modules = {}
    for page in pages:
        lines = page["text"].splitlines()
        # Le sommaire contient de nombreuses lignes à points de conduite.
        if sum(bool(re.search(r"(?:\.\s*){6,}", line)) for line in lines) > 3:
            continue
        for idx, line in enumerate(lines):
            match = HEADER.match(line)
            if not match:
                continue
            kind, code, title = match.group("kind", "code", "title")
            kind = "ressource" if kind.lower() == "ressource" else "sae"
            code = re.sub(r"\s+", "", code.upper())
            title = clean(title)
            # Une fiche peut avoir un titre réparti sur plusieurs lignes.
            for following in lines[idx + 1:idx + 3]:
                following = clean(following)
                if (not following or ":" in following or HEADER.match(following)
                        or re.match(r"(?:Compétence|Objectif|Descriptif|Apprentissage|Volume|Parcours|Mots|Semestre|©)", following, re.I)):
                    break
                if title.endswith("-"):
                    title = title[:-1] + following
                elif len(title) > 75 and not title.endswith((".", ":")):
                    title += " " + following
                else:
                    break
            if len(title) < 4 or re.search(r"(?:\.\s*){4,}", title):
                continue
            key = (code, title)
            modules.setdefault(key, {"kind": kind, "code": code, "title": title,
                                     "page": page["page"], "evidence": page["text"],
                                     "url": source["url"] + f"#page={page['page']}"})
    rome_mentions = {}
    for page in pages:
        for code in re.findall(r"\b[A-N]\d{4}\b", page["text"]):
            rome_mentions.setdefault(code, []).append(page["page"])
    programme = {**source, "sha256": digest, "page_count": len(pages),
                 "cover": pages[0]["text"], "modules": list(modules.values()),
                 "rome_mentions": rome_mentions,
                 "extraction": "pypdf; pages physiques PDF (base 1); texte brut, lecture des tableaux non garantie"}
    write_json(cached, {"sha256": digest, "pages": pages, "programme": programme})
    print(f"OK {source['id']}: {len(pages)} pages, {len(modules)} fiches pédagogiques, {len(rome_mentions)} codes ROME cités", flush=True)
    return programme


def main():
    sources = json.loads((ROOT / "data/but-sources.json").read_text(encoding="utf-8"))
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
        programmes = list(pool.map(extract, sources))
    write_json(ROOT / "data/but-programmes.json", programmes)
    if any(not p["modules"] or p["page_count"] < 10 for p in programmes):
        raise SystemExit("Extraction incomplète : vérifier les programmes sans fiches pédagogiques")


if __name__ == "__main__":
    main()
