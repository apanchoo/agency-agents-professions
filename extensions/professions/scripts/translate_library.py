"""Cache English translations of public professional vocabulary and descriptions."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import re
import threading
import time
import urllib.parse
import urllib.request
import zipfile

from editorial import RECIPES, DOMAINS

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data/translations-en.json"


def public_strings():
    with zipfile.ZipFile(ROOT / "sources/rome-official.zip") as archive:
        member = next(n for n in archive.namelist() if "fiche_emploi_metier" in n)
        records = json.loads(archive.read(member).decode("iso-8859-15"))
    values = set()
    for record in records:
        values.update([record["rome"]["intitule"], record["definition"]])
        values.update(a["libelle"] for a in record.get("appellations", []))
        for category in record.get("competences", {}).values():
            for group in category.get("enjeux", category.get("categories", [])):
                if group["libelle"] == "Certifications et habilitations":
                    continue
                values.add(group["libelle"])
                values.update(i["libelle"] for i in group.get("items", []))
        values.update(i["libelle"] for g in record.get("contextes_travail", []) for i in g.get("items", []))
        values.update(i["libelle"] for i in record.get("secteurs_activite", []))
    programmes = json.loads((ROOT / "data/but-programmes.json").read_text(encoding="utf-8"))
    values.update(m["title"] for p in programmes for m in p["modules"])
    for steps, outputs, checks in RECIPES.values():
        values.update(steps + outputs + checks)
    for label, _, outputs in DOMAINS.values():
        values.add(label)
        values.update(outputs)
    values.update([
        "Qualifier la demande, les données disponibles et les limites de l'assistance",
        "Sélectionner les activités réellement utiles à la demande",
        "Produire le support documentaire, l'analyse ou la préparation demandée",
        "Confronter le livrable aux pièces disponibles et signaler les contrôles restant à réaliser",
        "Les informations constatées sont séparées des hypothèses",
        "Chaque conclusion possède une preuve ou une vérification proposée",
        "Les interventions physiques et validations professionnelles restent identifiées comme telles",
    ])
    return sorted(v for v in values if v and v.strip())


def main():
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    pending = [v for v in public_strings() if v not in cache]
    batches, batch, size = [], [], 0
    for value in pending:
        if batch and size + len(value) > 3800:
            batches.append(batch)
            batch, size = [], 0
        batch.append(value)
        size += len(value) + 20
    if batch:
        batches.append(batch)
    print(f"Public text units: {len(pending)}; requests: {len(batches)}", flush=True)

    def translate(batch):
        text = "\n".join(f"[[{i:06d}]]\n{value}" for i, value in enumerate(batch))
        url = "https://translate.googleapis.com/translate_a/single?" + urllib.parse.urlencode({"client": "gtx", "sl": "fr", "tl": "en", "dt": "t", "q": text})
        for attempt in range(4):
            try:
                request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(request, timeout=60) as response:
                    data = json.load(response)
                result = "".join(row[0] for row in data[0] if row[0])
                matches = list(re.finditer(r"\[\[\s*(\d{6})\s*\]\]", result))
                if [int(m[1]) for m in matches] != list(range(len(batch))):
                    raise ValueError("Translation boundaries not preserved")
                translated = [result[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(result)].strip() for i, m in enumerate(matches)]
                if not all(translated):
                    raise ValueError("Empty translation")
                return dict(zip(batch, translated))
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(2 ** attempt)

    errors = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(translate, batch): batch for batch in batches}
        for i, future in enumerate(as_completed(futures), 1):
            try:
                cache.update(future.result())
            except Exception as exc:
                errors.append({"count": len(futures[future]), "error": type(exc).__name__ + ": " + str(exc)[:120]})
            if i % 10 == 0 or i == len(batches):
                CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                print(f"Translation batches: {i}/{len(batches)}; cached: {len(cache)}; failures: {len(errors)}", flush=True)
    (ROOT / "data/translation-errors.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if errors:
        raise SystemExit(f"{len(errors)} batches need retry; completed translations have been cached")


if __name__ == "__main__":
    main()
