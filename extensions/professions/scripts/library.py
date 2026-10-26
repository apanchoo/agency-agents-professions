"""Recherche, export sélectif et validation de la bibliothèque locale."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys
import zipfile

from build_library import ROOT, load, normalize, read_rome
from runtime_profiles import folder_name


ORIGIN_MARKERS = re.compile(r"\bROME\b|France\s+Travail|P[oô]le[- ]emploi|\bBUT\b|B\.?U\.?T\.?|SAÉ|\bOGR\b|enseignementsup-recherche|francetravail|agency-agents|\b(?:R\d+\.[A-Z0-9.]+|AC\d+\.\d+)\b")


def runtime_issues(paths):
    issues = []
    for path in paths:
        body = path.read_text(encoding="utf-8")
        marker = ORIGIN_MARKERS.search(body)
        if marker:
            issues.append(f"Origine de fabrication exposée : {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path.name} : {marker.group()}")
        if re.search(r"\]\([^)]*(?:audit/|sources/|programmes/|provenance\.json|fiche\.json|but\.md|rome\.md)", body):
            issues.append(f"Lien de provenance dans un fichier opérationnel : {path.name}")
    return issues


def search(query, but=None):
    term = normalize(query)
    return [r for r in load(ROOT / "catalog.json")
            if term in normalize(" ".join([r["code"], r["title"], r.get("original_title", ""), *r["appellations"], *r.get("original_appellations", [])]))
            and (not but or but in r["but"])]


def export_profile(code, destination):
    code = code.upper()
    if not re.fullmatch(r"[A-N]\d{4}", code):
        raise ValueError("Utiliser un code ROME de cinq caractères, par exemple M1805")
    row = next((r for r in load(ROOT / "catalog.json") if r["code"] == code), None)
    if row is None:
        raise ValueError(f"Fiche absente : {code}")
    target = Path(destination).resolve()
    if target.exists():
        raise FileExistsError(f"Destination déjà existante, choisir un nouveau dossier : {target}")
    # Conserver la structure : les liens AGENTS.md -> skills restent valides.
    target.mkdir(parents=True)
    agent_target = target / row["agent"]
    agent_target.parent.mkdir(parents=True)
    shutil.copy2(ROOT / row["agent"], agent_target)
    source_skill = (ROOT / row["skill"]).parent
    shutil.copytree(source_skill, target / Path(row["skill"]).parent)
    (target / "README.md").write_text(
        f"# {row['title']}\n\nProfil : [{row['agent']}]({row['agent']}).\n\n"
        f"Skill autonome : [{row['skill']}]({row['skill']}).\n\n"
        "Detailed expertise, methods and validation scenarios are included. "
        "The export does not change configuration or start an agent.\n",
        encoding="utf-8")
    (target / "audit").mkdir()
    shutil.copytree(ROOT / f"audit/metiers/{code}", target / f"audit/metiers/{code}")
    shutil.copy2(ROOT / "sources/rome-license.pdf", target / "audit/rome-license.pdf")
    shutil.copy2(ROOT / "ATTRIBUTION.md", target / "audit/ATTRIBUTION.md")
    return target


def validate(official_validator=None):
    errors = []
    catalog = load(ROOT / "catalog.json")
    fiches, metadata, source = read_rome()
    expected = {f["rome"]["code_rome"]: f for f in fiches}
    if len(catalog) != len(expected) or {r["code"] for r in catalog} != set(expected):
        errors.append("Le catalogue ne correspond pas exactement à l'export ROME")
    programmes = {p["id"]: p for p in load(ROOT / "data/but-programmes.json")}
    if len(programmes) != 24:
        errors.append("Les 24 spécialités BUT ne sont pas toutes présentes")
    # Empreinte et type réel des sources, pas seulement un fichier présent.
    for row in load(ROOT / "sources/manifest.json"):
        payload = (ROOT / row["path"]).read_bytes()
        if hashlib.sha256(payload).hexdigest() != row["sha256"]:
            errors.append(f"Empreinte source différente : {row['path']}")
        if row["path"].endswith(".pdf") and not payload.startswith(b"%PDF-"):
            errors.append(f"Faux PDF : {row['path']}")
    validator = None
    if official_validator:
        sys.path.insert(0, str(ROOT / ".tools"))
        spec = importlib.util.spec_from_file_location("codex_skill_validator", official_validator)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        validator = module.validate_skill
    else:
        sys.path.insert(0, str(ROOT / ".tools"))
        import yaml
    local_links_checked = 0
    covered_but = Counter()
    for index, row in enumerate(catalog, 1):
        if index % 300 == 0:
            print(f"Validation : {index}/{len(catalog)} métiers", flush=True)
        code = row["code"]
        skill = ROOT / row["skill"]
        audit = ROOT / f"audit/metiers/{code}"
        if load(audit / "fiche.json") != expected[code]:
            errors.append(f"Le contenu ROME a été altéré : {code}")
        text = skill.read_text(encoding="utf-8")
        expected_name = folder_name(code, row.get("original_title", row["title"]))
        if skill.parent.name != expected_name or Path(row["agent"]).parent.name != expected_name:
            errors.append(f"Dossier sans nom de métier cohérent : {code}")
        runtime_paths = [ROOT / row["agent"], *skill.parent.rglob("*.md")]
        errors.extend(runtime_issues(runtime_paths))
        if any(p.is_file() and p.suffix != ".md" for p in skill.parent.rglob("*")):
            errors.append(f"Métadonnées non opérationnelles dans le skill : {code}")
        if validator:
            valid, message = validator(skill.parent)
            if not valid:
                errors.append(f"{code} : {message}")
        else:
            header = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            if not header:
                errors.append(f"Frontmatter absent : {code}")
                continue
            front = yaml.safe_load(header[1])
            if front.get("name") != skill.parent.name or not front.get("description"):
                errors.append(f"Frontmatter incohérent : {code}")
            if len(front.get("description", "")) > 1024:
                errors.append(f"Description trop longue : {code}")
        for path in runtime_paths:
            body = path.read_text(encoding="utf-8")
            for link in re.findall(r"\]\(([^)]+)\)", body):
                if "://" in link or link.startswith("#"):
                    continue
                if not (path.parent / link.split("#")[0]).is_file():
                    errors.append(f"Lien local invalide : {code} : {link}")
                local_links_checked += 1
        provenance = load(audit / "provenance.json")
        if provenance["rome"] != source or provenance["rome_metadata"] != metadata[code]:
            errors.append(f"Provenance ROME incohérente : {code}")
        for match in provenance["but"]:
            programme = programmes[match["programme_id"]]
            covered_but[programme["id"]] += 1
            if match["programme_sha256"] != programme["sha256"]:
                errors.append(f"Empreinte BUT incohérente : {code}")
            module_keys = {(m["code"], m["title"], m["page"]) for m in programme["modules"]}
            for m in match["modules"]:
                if (m["code"], m["title"], m["page"]) not in module_keys:
                    errors.append(f"Module pédagogique sans preuve : {code} {m['code']}")
                if not 1 <= m["page"] <= programme["page_count"] or not m["shared_terms"]:
                    errors.append(f"Module pédagogique sans pertinence ni page valide : {code}")
    actual_agents = list((ROOT / "agents").glob("*/AGENTS.md"))
    actual_skills = list((ROOT / "skills").glob("*/SKILL.md"))
    if len(actual_agents) != len(expected) or len(actual_skills) != len(expected):
        errors.append("Des agents ou skills sont manquants ou surnuméraires")
    report = {"status": "passed" if not errors else "failed", "agents": len(actual_agents),
              "skills": len(actual_skills), "but_programmes": len(programmes),
              "local_links_checked": local_links_checked,
              "runtime_origin_references": "checked_absent",
              "profession_folder_names": "checked",
              "official_skill_validator": str(official_validator) if official_validator else None,
              "semantic_review": "Échantillon relu ; pas de validation métier humaine exhaustive.",
              "errors": errors}
    (ROOT / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def bundle(destination):
    destination = Path(destination).resolve()
    if destination.exists():
        raise FileExistsError(f"Archive déjà existante : {destination}")
    count = 0
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(ROOT.rglob("*")):
            relative = path.relative_to(ROOT)
            if not path.is_file() or path == destination or any(p in {".tools", "__pycache__", "tmp", "exports"} for p in relative.parts):
                continue
            archive.write(path, str(Path("rome-agency") / relative))
            count += 1
    return {"archive": str(destination), "files": count, "bytes": destination.stat().st_size,
            "sha256": hashlib.sha256(destination.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("--but")
    p = sub.add_parser("export")
    p.add_argument("code")
    p.add_argument("--destination", required=True)
    p = sub.add_parser("validate")
    p.add_argument("--official-validator", type=Path)
    p = sub.add_parser("bundle")
    p.add_argument("--destination", required=True)
    args = parser.parse_args()
    if args.command == "search":
        print(json.dumps(search(args.query, args.but), ensure_ascii=False, indent=2))
    elif args.command == "export":
        print(export_profile(args.code, args.destination))
    elif args.command == "bundle":
        print(json.dumps(bundle(args.destination), ensure_ascii=False, indent=2))
    else:
        report = validate(args.official_validator)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if report["errors"]:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
