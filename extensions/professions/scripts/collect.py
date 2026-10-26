"""Collecte reproductible de sources publiques, sans authentification."""
from __future__ import annotations

import concurrent.futures
import datetime as dt
import hashlib
import json
from pathlib import Path
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/"
PROGRAMMES = [
    ("cj", "Carrières juridiques", "carri-res-juridiques-30816.pdf"),
    ("cs", "Carrières sociales", "carri-res-sociales-30819.pdf"),
    ("chimie", "Chimie", "chimie-30822.pdf"),
    ("gb", "Génie biologique", "g-nie-biologique-30825.pdf"),
    ("gcgp", "Génie chimique - Génie des procédés", "g-nie-chimique-g-nie-des-proc-d-s-30828.pdf"),
    ("gccd", "Génie civil - Construction durable", "g-nie-civil-construction-durable-30831.pdf"),
    ("geii", "Génie électrique et informatique industrielle", "g-nie-lectrique-et-informatique-industrielle-30834.pdf"),
    ("gim", "Génie industriel et maintenance", "g-nie-industriel-et-maintenance-30837.pdf"),
    ("gmp", "Génie mécanique et productique", "g-nie-m-canique-et-productique-30840.pdf"),
    ("gaco", "Gestion administrative et commerciale des organisations", "gestion-administrative-et-commerciale-des-organisations-30843.pdf"),
    ("gea", "Gestion des entreprises et des administrations", "gestion-des-entreprises-et-des-administrations-30846.pdf"),
    ("hse", "Hygiène - Sécurité - Environnement", "hygi-ne-s-curit--environnement-30849.pdf"),
    ("infocom", "Information - Communication", "information-communication-30852.pdf"),
    ("info", "Informatique", "informatique-30855.pdf"),
    ("mlt", "Management de la logistique et des transports", "management-de-la-logistique-et-des-transports-30858.pdf"),
    ("mp", "Mesures physiques", "mesures-physiques-30861.pdf"),
    ("mt2e", "Métiers de la transition et de l'efficacité énergétiques", "m-tiers-de-la-transition-et-de-l-efficacit-nerg-tiques-30864.pdf"),
    ("mmi", "Métiers du multimédia et de l'Internet", "m-tiers-du-multim-dia-et-de-l-internet-30867.pdf"),
    ("pec", "Packaging, emballage et conditionnement", "packaging-emballage-et-conditionnement-30870.pdf"),
    ("qlio", "Qualité, logistique industrielle et organisation", "qualit-logistique-industrielle-et-organisation-30873.pdf"),
    ("rt", "Réseaux et télécommunications", "r-seaux-et-t-l-communications-30876.pdf"),
    ("sd", "Science des données", "science-des-donn-es-30879.pdf"),
    ("sgm", "Science et génie des matériaux", "science-et-g-nie-des-mat-riaux-30882.pdf"),
    ("tc", "Techniques de commercialisation", "techniques-de-commercialisation-30885.pdf"),
]
def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    manifest_path = ROOT / "sources/manifest.json"
    old = {x["path"]: x for x in read_json(manifest_path)} if manifest_path.exists() else {}
    jobs = [("sources/rome-official.zip", "https://api.francetravail.fr/api-nomenclatureemploi/v1/open-data/json", "France Travail", "Export intégral JSON ROME"),
            ("sources/rome-license.pdf", "https://www.francetravail.org/files/live/sites/peorg/files/documents/Statistiques-et-analyses/Open-data/ROME/rome_licence_ouverte.pdf", "France Travail", "Licence ROME"),
            ("sources/agency-example.md", "https://raw.githubusercontent.com/msitarzewski/agency-agents/main/engineering/engineering-frontend-developer.md", "msitarzewski/agency-agents", "Exemple de structure, non recopié dans les profils"),
            ("sources/agency-LICENSE", "https://raw.githubusercontent.com/msitarzewski/agency-agents/main/LICENSE", "msitarzewski/agency-agents", "Licence MIT du modèle d'inspiration")]
    jobs.extend((f"sources/but/{key}.pdf", BASE + filename, "Ministère de l'Enseignement supérieur", title) for key, title, filename in PROGRAMMES)

    def fetch(job):
        relative, url, producer, title = job
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            request = urllib.request.Request(url, headers={"User-Agent": "ROME-Agency/1.0 (public educational reference collection)"})
            with urllib.request.urlopen(request, timeout=120) as response:
                payload = response.read()
                last_modified = response.headers.get("Last-Modified")
            if relative.endswith(".pdf") and not payload.startswith(b"%PDF-"):
                raise ValueError(f"Ce téléchargement n'est pas un PDF : {url}")
            if relative.endswith(".zip") and not payload.startswith(b"PK"):
                raise ValueError(f"Ce téléchargement n'est pas un ZIP : {url}")
            path.write_bytes(payload)
        else:
            payload = path.read_bytes()
            last_modified = old.get(relative, {}).get("last_modified")
        digest = hashlib.sha256(payload).hexdigest()
        row = {"path": relative, "url": url, "producer": producer, "title": title,
               "sha256": digest, "bytes": len(payload), "verified_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
               "last_modified": last_modified}
        print(f"OK {relative} {len(payload)}", flush=True)
        return row

    rows, failures = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        pending = {pool.submit(fetch, job): job for job in jobs}
        for future in concurrent.futures.as_completed(pending):
            try:
                rows.append(future.result())
            except Exception as exc:
                failures.append({"path": pending[future][0], "error": str(exc)})
                print(f"ERREUR {pending[future][0]} : {exc}", flush=True)
    write_json(manifest_path, sorted(rows, key=lambda x: x["path"]))
    write_json(ROOT / "sources/collection-errors.json", failures)
    write_json(ROOT / "data/but-sources.json", [{"id": key, "title": title, "url": BASE + filename, "pdf": f"sources/but/{key}.pdf"} for key, title, filename in PROGRAMMES])
    with zipfile.ZipFile(ROOT / "sources/rome-official.zip") as archive:
        version = archive.read("version.txt").decode("utf-8-sig")
    (ROOT / "sources/rome-version.txt").write_text(version, encoding="utf-8")
    if failures:
        raise SystemExit(f"{len(failures)} source(s) non récupérée(s), voir sources/collection-errors.json")


if __name__ == "__main__":
    main()
