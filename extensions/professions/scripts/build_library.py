"""Génère un profil AGENTS.md et un skill autonome par fiche ROME officielle."""
from __future__ import annotations

from collections import Counter
import hashlib
import html
import json
import math
from pathlib import Path
import re
import unicodedata
import zipfile

from editorial import DOMAINS
from runtime_profiles import folder_name, generate_profile, expertise_content, practice_content
from editorial import recipe_for
from english import tr
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[1]
ROME_URL = "https://api.francetravail.fr/api-nomenclatureemploi/v1/open-data/json"
ROME_PAGE = "https://www.francetravail.org/opendata/repertoire-operationnel-des-meti.html?type=article"
BUT_PAGE = "https://www.enseignementsup-recherche.gouv.fr/fr/lp-86602"
SPECIFIC = {
    "cj": "jurid|jurist|notair|droit|contentieux|greff|huissier|justice|judiciaire",
    "cs": "social|socioculturel|educat|insertion",
    "chimie": "chimi|formul",
    "gb": "biologi|biotech|agronom|dietet|nutrition|ecolog|agricol|aliment",
    "gcgp": "procede|process|bioproduction",
    "gccd": "batiment|construction|genie civil|travaux public|rehabilitation|beton|geometr|topograph",
    "geii": "electri|electron|automati|embarque|robot",
    "gim": "maintenance.*industri|maintenicien|pluritech",
    "gmp": "mecani|producti|usinage|methodes.*industri|industrialisation",
    "gaco": "entrepreneuri|directeur.*entreprise|directrice.*entreprise|assistant.*gestion",
    "gea": "comptab|fiscal|financ|ressources humaines|paie|controle.*gestion",
    "hse": "risque|securite|prevention|hygiene|qse|hse",
    "infocom": "communication|journal|documentation|publicite|livre|patrimoine|bibliothe|editorial",
    "info": "developpe|logiciel|application|programm|informatique",
    "mlt": "logist|transport|supply|affret|mobilite",
    "mp": "mesure|metrolog|instrument|essai|physique",
    "mt2e": "energe|thermi|climat|chauff|froid|fluid|ventilation",
    "mmi": "web|multimedia|graph|design|internet|experience utilisateur|community",
    "pec": "emball|packaging|conditionnement",
    "qlio": "qualite|logist|ordonnancement|planification|approvisionnement",
    "rt": "reseau|telecom|cyber|cloud",
    "sd": "statisti|donnee|data|decisionnel|actuari|econometr",
    "sgm": "materiau|materiaux|composite|polymere|metallur|plastur|cerami|recycl",
    "tc": "commercial|marketing|vente|client|marque|achat|commerce|distribution",
}
PARCOURS = {
    "info": [(r"developpe|logiciel|programm", "REAL"), (r"donnee|data", "ADMIN"), (r"reseau|systeme|infrastructure", "DEPLOI")],
    "cs": [(r"assistant.*social|assistante.*social", "AS"), (r"educat.*special", "ES"), (r"animation|animateur|animatrice", "ASSC"), (r"territoir|ville", "VTD"), (r"etablissement.*sani|etablissement.*social", "CGE3S")],
    "geii": [(r"electron|embarque", "ESE"), (r"automati|robot", "AII"), (r"electri|energie", "EME")],
    "gb": [(r"dietet|nutrition", "DN"), (r"agricol|agronom", "AGRO"), (r"biomed|biotech|laboratoire.*medical", "BMB"), (r"aliment", "SAB"), (r"environnement|ecolog", "SEE")],
    "gea": [(r"comptab|fiscal", "GC2F"), (r"ressources humaines|paie", "GPRH"), (r"controle.*gestion", "CG2P")],
    "mmi": [(r"web|developpe", "DWEB-DI"), (r"design|graph|creat", "CREA"), (r"community|marketing|communication", "STRAT-UX")],
    "rt": [(r"cyber|securite", "CYBER"), (r"cloud|devops", "DSC"), (r"iot|objet.*connect", "IOM"), (r"telecom", "ROM")],
    "sd": [(r"statisti|actuari", "EMS"), (r"decisionnel|data.*engineer|ingenieur.*donnee", "VCOD")],
}
STOP = set("a au aux avec ce ces cette cet dans de des du en et est etre faire la le les leur lors ou par pour que qui sa se ses son sur un une vos votre vous il elle ils elles ainsi afin aux entre mais tout tous toute toutes plus moins comme selon sans dont sous puis apres avant metier professionnel professionnelle professionnels professionnelles activite activites competence competences capacite capacites maitriser comprendre connaissance connaissances objectif objectifs apprentissage apprentissages critique critiques ressource ressources semestre parcours formation programme national but situation situations evaluation realiser mettre oeuvre developper participer contribuer utiliser analyser concevoir organiser assurer gerer controler suivre projet projets besoin besoins technique techniques pratique pratiques outil outils methode methodes introduction initiation base bases fondamentaux fondamental approfondissement perfectionnement generale general generaux environnement notamment niveau niveaux compte prise prendre adapter respect regle regles qualite service services entreprise entreprises organisation organisations gestion communication equipe travail systeme systemes processus developpement donnee donnees information informations resultat resultats donnes domaine domaines contexte contextes necessaire necessaires permet permettre savoir savoirs premier premiere deux trois quatre cinq six annee annuel etude etudes commun commune communes communs associe associes associees associee composante composantes essentiel essentielles essentiels essentielle professionnellement personne personnes cadre demarche demarches analyse differents differentes different objectifs evaluation evaluee apprentissage enseignement ministere superieur recherche innovation francais anglais langue langages page baccalaureat dut licence professionnelle semestre semestres rapport suite exemple exemples francetravail".split())


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def normalize(text):
    return "".join(c for c in unicodedata.normalize("NFKD", text.lower()) if not unicodedata.combining(c))


def tokens(text):
    values = re.findall(r"[a-z][a-z0-9]{2,}", normalize(text))
    stems = {v[:-1] if len(v) > 5 and v.endswith("s") else v for v in values if v not in STOP and not v.startswith("ac0")}
    return stems - STOP - {"langue", "langag", "oral", "orale", "ecrit", "ecrite", "ecrits", "ecrites", "langues", "profession", "internationale", "international", "fondamental", "techniqu", "scientifique"}


@lru_cache(maxsize=5000)
def module_tokens(title, evidence):
    return tokens(title), tokens(evidence)


def flatten_competences(fiche, kind="savoir_faire"):
    part = fiche.get("competences", {}).get(kind, {})
    groups = part.get("enjeux", part.get("categories", []))
    return [{**item, "group": group["libelle"]} for group in groups for item in group.get("items", [])]


def read_rome():
    with zipfile.ZipFile(ROOT / "sources/rome-official.zip") as archive:
        names = [n for n in archive.namelist() if "fiche_emploi_metier" in n and n.endswith(".json")]
        if len(names) != 1:
            raise ValueError(f"Export ROME ambigu : {names}")
        raw = archive.read(names[0])
        # Les JSON v462 sont ISO-8859-15 ; version.txt est UTF-8.
        try:
            decoded = raw.decode("utf-8-sig")
            encoding = "utf-8-sig"
        except UnicodeDecodeError:
            decoded = raw.decode("iso-8859-15")
            encoding = "iso-8859-15"
        fiches = json.loads(decoded)
        version_text = archive.read("version.txt").decode("utf-8-sig")
        meta_name = next(n for n in archive.namelist() if "referentiel_code_rome" in n)
        metadata = json.loads(archive.read(meta_name).decode(encoding))
    version_match = re.search(r"Numero de version\s*:\s*(\d+)", version_text)
    date_match = re.search(r"Date de publication\s*:\s*(\S+)", version_text)
    if not version_match or not date_match:
        raise ValueError("Version ou date de publication absente de l'export")
    return fiches, {m["code_rome"]: m for m in metadata}, {
        "producer": "France Travail (anciennement Pôle emploi)", "version": version_match[1],
        "published": date_match[1], "archive": "sources/rome-official.zip", "member": names[0],
        "encoding": encoding, "url": ROME_URL,
        "sha256": hashlib.sha256((ROOT / "sources/rome-official.zip").read_bytes()).hexdigest()}


def choose_modules(fiche, programme, idf):
    title = fiche["rome"]["intitule"]
    focus = next((path for pattern, path in PARCOURS.get(programme["id"], []) if re.search(pattern, normalize(title))), None)
    primary = [c for c in flatten_competences(fiche) if c.get("coeur_metier")]
    technical = [c for c in flatten_competences(fiche, "savoirs") if c["group"] != "Certifications et habilitations"]
    query = tokens(title + " " + fiche["definition"] + " " + " ".join(c["libelle"] for c in primary + technical))
    scored = []
    for module in programme["modules"]:
        title_tokens, evidence_tokens = module_tokens(module["title"], module["evidence"])
        shared = query & title_tokens
        if not shared:
            continue
        score = sum(idf.get(t, 1) ** 2 for t in shared) / math.sqrt(max(len(title_tokens), 1))
        # Les intitulés sont plus discriminants que les AC récurrents du texte complet.
        score += 0.04 * sum(idf.get(t, 1) for t in query & evidence_tokens)
        path_parts = module["code"].split(".")[1:-1]
        if focus and path_parts:
            score *= 1.8 if focus in path_parts else 0.35
        scored.append((score, module, sorted(shared)))
    selected = []
    for kind, count in [("ressource", 3), ("sae", 2)]:
        seen_codes = set()
        seen_titles = set()
        for score, module, shared in sorted(scored, key=lambda x: (-x[0], x[1]["page"])):
            if module["kind"] != kind or module["code"] in seen_codes or normalize(module["title"]) in seen_titles:
                continue
            selected.append({**module, "selection_score": round(score, 4), "shared_terms": shared})
            seen_codes.add(module["code"])
            seen_titles.add(normalize(module["title"]))
            if len(seen_codes) == count:
                break
    return selected


def match_programmes(fiche, meta, programmes, rules, idf):
    code = fiche["rome"]["code_rome"]
    title_text = normalize(fiche["rome"]["intitule"])
    title_definition = normalize(fiche["rome"]["intitule"] + " " + fiche["definition"])
    matches = []
    for programme in programmes:
        rule = rules[programme["id"]]
        direct_pages = programme["rome_mentions"].get(code, [])
        parent = meta.get("code_rome_parent")
        parent_pages = programme["rome_mentions"].get(parent, []) if parent != code else []
        terms = sorted(set(m.group() for m in re.finditer(rule["terms"], title_definition)))
        allowed_prefix = any(code.startswith(prefix) for prefix in rule["prefixes"])
        # Un parent ROME ancien peut englober de nombreux nouveaux métiers :
        # sa citation ne suffit pas sans rapprochement thématique indépendant.
        if not (allowed_prefix and terms):
            continue
        modules = choose_modules(fiche, programme, idf)
        if not modules:
            continue
        if direct_pages:
            basis, priority = "code_rome_cite_dans_programme", 5
        elif parent_pages:
            basis, priority = "code_parent_rome_cite_dans_programme", 1
        else:
            basis, priority = "rapprochement_editorial_domaine_et_termes", 0
        title_terms = sorted(set(m.group() for m in re.finditer(rule["terms"], title_text)))
        specific_terms = sorted(set(m.group() for m in re.finditer(SPECIFIC[programme["id"]], title_text)))
        # La pertinence métier prime sur la simple présence d'un code dans une
        # liste de débouchés. Les termes du titre pèsent davantage que les savoirs.
        score = (priority + 60 * len(specific_terms) + 15 * len(title_terms) + 3 * len(terms)
                 + 3 * math.log1p(sum(m["selection_score"] for m in modules) / len(modules)))
        matches.append({"programme_id": programme["id"], "title": programme["title"],
                        "basis": basis, "reviewed_by_human": False, "score": round(score, 3),
                        "matched_terms": terms, "direct_rome_pages": direct_pages, "parent_rome": parent,
                        "title_terms": title_terms, "specific_title_terms": specific_terms,
                        "parent_rome_pages": parent_pages, "modules": modules,
                        "programme_url": programme["url"], "programme_sha256": programme["sha256"]})
    return sorted(matches, key=lambda x: (-x["score"], x["programme_id"]))[:3]


def bullet(items):
    return "\n".join("- " + str(item).replace("\n", " ") for item in items)


def activity_text(items):
    return bullet(f"{c['libelle']} (OGR {c['code_ogr']}, {c['group']})" for c in items)


def evidence_for(activity):
    value = normalize(activity)
    for pattern, evidence in [
        (r"^(analyser|diagnostiquer|evaluer|identifier|etudier)", "Diagnostic reliant données d'entrée, constats et interprétations ; hypothèses séparées."),
        (r"^(concevoir|dessiner|modeliser|dimensionner|definir)", "Spécification, modèle ou plan relié aux exigences ; choix et calculs vérifiables."),
        (r"^(tester|controler|verifier|mesurer|surveiller)", "Protocole avec critère attendu, résultat disponible et écart ; indiquer les mesures restant à réaliser."),
        (r"^(developper|programmer|integrer|deployer)", "Livrable technique et scénario de recette reproductible ; erreurs et dépendances explicites."),
        (r"^(planifier|organiser|coordonner|piloter|superviser)", "Plan avec ressources, dépendances, responsabilités, jalons et mesure de réalisation."),
        (r"^(rediger|documenter|maintenir.*documentation|communiquer|presenter)", "Document utilisable par son destinataire avec sources, date et périmètre."),
        (r"^(conseiller|accompagner|orienter|accueillir)", "Analyse du besoin exprimé, options et support d'accompagnement adapté au public."),
        (r"^(reparer|entretenir|conduire|installer|fabriquer|effectuer|preparer|realiser)", "Préparation ou gamme avec points de contrôle ; observation physique et validation terrain attribuées à leur auteur réel."),
    ]:
        if re.search(pattern, value):
            return evidence
    return "Support produit et preuve de son usage attendu ; contrôle proposé pour les points non vérifiés."


def rome_reference(fiche, source, meta):
    code, title = fiche["rome"]["code_rome"], fiche["rome"]["intitule"]
    parts = [f"# {code} — {title}",
             f"Source : France Travail, ROME 4.0 v{source['version']}, publication {source['published']}.\n"
             f"[Page officielle]({ROME_PAGE}) · [Export JSON]({ROME_URL})\n\n"
             f"Membre ZIP : `{source['member']}` ; SHA-256 archive : `{source['sha256']}`.\n"
             "Les données ci-dessous sont celles de la fiche ; les consignes de l'agent sont une adaptation distincte.",
             "## Définition\n\n" + fiche["definition"],
             "## Accès au métier\n\n" + fiche["acces_metier"],
             "## Tags du référentiel\n\n" + bullet(f"{k} : {v if v is not None else 'non renseigné'}" for k, v in meta.items() if k.startswith(("transition", "emploi_", "code_rome_parent"))),
             "## Appellations\n\n" + bullet(f"{a['libelle']} (OGR {a['code_ogr']})" for a in fiche["appellations"])]
    for kind, name in [("savoir_faire", "Savoir-faire"), ("savoir_etre_professionnel", "Savoir-être"), ("savoirs", "Savoirs")]:
        items = flatten_competences(fiche, kind)
        parts.append(f"## {name}\n\n" + bullet(f"{c['libelle']} — {c['group']} ; OGR {c['code_ogr']} ; cœur métier : {c.get('coeur_metier') or 'non indiqué'}" for c in items))
    parts.append("## Contextes de travail\n\n" + bullet(f"{g['libelle']} : {i['libelle']} (OGR {i['code_ogr']})" for g in fiche.get("contextes_travail", []) for i in g.get("items", [])))
    parts.append("## Secteurs\n\n" + bullet(x["libelle"] for x in fiche.get("secteurs_activite", [])))
    parts.append("## Mobilités (source ROME, pas une délégation automatique)\n\n" + bullet(x["rome_cible"] for x in fiche.get("mobilites", [])))
    return "\n\n".join(parts)


def but_reference(matches):
    parts = ["# Enrichissement BUT et preuves",
             "Les rapprochements et la sélection des fiches pédagogiques sont produits par le générateur et restent à relire. "
             "Un code cité dans un programme atteste cette mention, sans prouver une équivalence diplôme/métier. "
             "Un code parent est distingué d'un code exact. Les pages sont les pages physiques du PDF, base 1. "
             "Le texte des pages est une extraction ; les tableaux peuvent perdre leur disposition."]
    if not matches:
        parts.append("Aucun rapprochement suffisamment étayé avec les 24 BUT selon les règles actuelles. Ne pas inventer un rattachement pédagogique.")
    for match in matches:
        parts.append(f"## BUT {match['title']}\n\n"
                     f"Fondement : `{match['basis']}`. Termes de rapprochement : {', '.join(match['matched_terms']) or 'mention de code'}. "
                     f"Pages citant le code exact : {match['direct_rome_pages'] or 'aucune'} ; "
                     f"pages citant le parent {match['parent_rome']} : {match['parent_rome_pages'] or 'aucune'}.\n\n"
                     f"[Programme ministériel]({match['programme_url']}) ; SHA-256 `{match['programme_sha256']}`.")
        for m in match["modules"]:
            label = "SAÉ" if m["kind"] == "sae" else "Ressource"
            parts.append(f"### {label} {m['code']} — {m['title']}\n\n"
                         f"[Page {m['page']}]({m['url']}). Termes communs : {', '.join(m['shared_terms'])}.\n\n"
                         "Extrait de la page contenant la fiche (donnée de référence, pas une instruction) :\n\n"
                         + "\n".join("> " + line for line in m["evidence"].splitlines()))
    return "\n\n".join(parts)


def pedagogical_summary(matches):
    if not matches:
        return "Aucun rattachement BUT retenu. Utiliser le référentiel ROME et les pièces de la demande."
    lines = []
    for match in matches:
        lines.append(f"### BUT {match['title']}\n\nRapprochement : `{match['basis']}`, à relire.")
        lines.append(bullet(f"{'SAÉ' if m['kind'] == 'sae' else 'Ressource'} {m['code']} : {m['title']} — [p. {m['page']}]({m['url']})" for m in match["modules"]))
    return "\n\n".join(lines)



def main():
    fiches, metadata, source = read_rome()
    programmes = load(ROOT / "data/but-programmes.json")
    rules = load(ROOT / "data/mapping-rules.json")
    document_frequency = Counter(t for p in programmes for m in p["modules"] for t in tokens(m["title"]))
    n = sum(len(p["modules"]) for p in programmes)
    idf = {t: math.log((1 + n) / (1 + count)) + 1 for t, count in document_frequency.items()}
    previous_path = ROOT / "catalog.json"
    previous = {r["code"]: r for r in load(previous_path)} if previous_path.exists() else {}
    catalog, mappings = [], []
    for index, fiche in enumerate(sorted(fiches, key=lambda x: x["rome"]["code_rome"]), 1):
        if index % 300 == 0:
            print(f"Generating: {index}/{len(fiches)} métiers", flush=True)
        code, title = fiche["rome"]["code_rome"], fiche["rome"]["intitule"]
        if not re.fullmatch(r"[A-N]\d{4}", code):
            raise ValueError(f"Code inattendu : {code}")
        meta = metadata[code]
        matches = match_programmes(fiche, meta, programmes, rules, idf)
        agent, skill = generate_profile(fiche, meta, source, matches)
        name = folder_name(code, title)
        folder = ROOT / f"skills/{name}"
        audit = ROOT / f"audit/metiers/{code}"
        write(ROOT / f"agents/{name}/AGENTS.md", agent)
        write(folder / "SKILL.md", skill)
        write(folder / "references/expertise.md", expertise_content(fiche))
        write(folder / "references/practice.md", practice_content(matches, *recipe_for(code, matches[0]["programme_id"] if matches else None)))
        for retired_reference in [folder / "references/metier.md", folder / "references/pratique.md"]:
            if retired_reference.is_file():
                retired_reference.unlink()
        dump(audit / "fiche.json", fiche)
        write(audit / "rome.md", rome_reference(fiche, source, meta))
        write(audit / "but.md", but_reference(matches))
        dump(audit / "provenance.json", {"rome": source, "rome_metadata": meta,
             "but": [{k: v for k, v in m.items() if k != "modules"} | {"modules": [{k: v for k, v in mod.items() if k != "evidence"} for mod in m["modules"]]} for m in matches],
             "editorial": "Workflows, livrables et critères proposés par le générateur ; pas une norme ni une équivalence officielle."})
        row = {"code": code, "title": tr(title), "original_title": title, "domain": code[0], "domain_title": tr(DOMAINS[code[0]][0]),
               "name": name, "agent": f"agents/{name}/AGENTS.md", "skill": f"skills/{name}/SKILL.md",
               "appellations": [tr(a["libelle"]) for a in fiche["appellations"]],
               "original_appellations": [a["libelle"] for a in fiche["appellations"]],
               "but": [m["programme_id"] for m in matches], "regulated": meta.get("emploi_reglemente"),
               "but_status": "propose_a_relire" if matches else "sans_rapprochement"}
        catalog.append(row)
        mappings.append({"code": code, "matches": [{k: v for k, v in m.items() if k != "modules"} | {"modules": [{k: v for k, v in mod.items() if k != "evidence"} for mod in m["modules"]]} for m in matches]})
        # Retirer uniquement les fichiers de l'ancien format généré. Les données
        # originales viennent d'être conservées dans audit/metiers/<code>.
        retired = [(code, "rome-" + code.lower())]
        old_name = previous.get(code, {}).get("name")
        if old_name and old_name != name and re.fullmatch(r"[a-z0-9-]+", old_name):
            retired.append((old_name, old_name))
        for old_agent_name, old_skill_name in retired:
            legacy_agent = ROOT / "agents" / old_agent_name
            legacy_skill = ROOT / "skills" / old_skill_name
            for old in [legacy_agent / "AGENTS.md", legacy_skill / "SKILL.md",
                        *(legacy_skill / "references" / filename for filename in ["fiche.json", "rome.md", "but.md", "provenance.json", "metier.md", "pratique.md", "expertise.md", "practice.md"])]:
                if old.is_file():
                    old.unlink()
            for old in [legacy_skill / "references", legacy_skill, legacy_agent]:
                if old.is_dir() and not any(old.iterdir()):
                    old.rmdir()
    dump(ROOT / "catalog.json", catalog)
    dump(ROOT / "data/rome-but-mapping.json", mappings)
    dump(ROOT / "data/rome-but-mentions.json", [{"programme_id": p["id"], "url": p["url"], "rome_mentions": p["rome_mentions"]} for p in programmes])
    dump(ROOT / "data/rome-source.json", source)
    coverage = {"rome_fiches": len(fiches), "agents": len(catalog), "skills": len(catalog),
                "but_programmes": len(programmes), "but_pdf_pages": sum(p["page_count"] for p in programmes),
                "pedagogical_records": n, "agents_with_but": sum(bool(r["but"]) for r in catalog),
                "agents_without_but": sum(not r["but"] for r in catalog),
                "by_but": dict(Counter(b for r in catalog for b in r["but"])),
                "by_domain": dict(Counter(r["domain"] for r in catalog)),
                "but_mapping_human_reviewed": False, "rome": source}
    dump(ROOT / "coverage.json", coverage)
    for p in programmes:
        modules = p["modules"]
        write(ROOT / f"programmes/{p['id']}.md", f"# BUT {p['title']}\n\n[PDF officiel]({p['url']}) ; {p['page_count']} pages ; SHA-256 `{p['sha256']}`.\n\n"
              + p["cover"] + "\n\n## Fiches pédagogiques repérées\n\n"
              + bullet(f"{'SAÉ' if m['kind'] == 'sae' else 'Ressource'} {m['code']} : {m['title']} — [p. {m['page']}]({m['url']})" for m in modules))
    write(ROOT / "CATALOG.md", "# Professional Agent Catalog\n\n"
          "Select a profession-specific agent and its companion skill.\n\n"
          "| Identifier | Profession | Profile | Skill | Domain |\n| --- | --- | --- | --- | --- |\n"
          + "\n".join(f"| {r['code']} | {r['title'].replace('|', '/')} | [AGENTS.md]({r['agent']}) | [SKILL.md]({r['skill']}) | {r['domain_title']} |" for r in catalog))
    # Navigateur local, autonome et hors ligne ; aucune donnée distante exécutée.
    payload = json.dumps(catalog, ensure_ascii=False).replace("<", "\\u003c")
    write(ROOT / "catalog.html", """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Professional Agents</title>
<style>body{font:16px system-ui;background:#f3f5f9;color:#142338;max-width:1200px;margin:36px auto;padding:0 24px}h1{font-size:36px}input,select{font:inherit;padding:12px;border:1px solid #bbc6d6;border-radius:8px;margin:4px 8px 12px 0}input{width:min(500px,90%)}table{width:100%;border-collapse:collapse;background:white}td,th{text-align:left;padding:14px;border-bottom:1px solid #dee4ee}a{color:#145cbb}small{color:#536079}#count{margin:12px 0}thead{background:#e6edf7}tr:hover{background:#f5f8ff}</style>
<h1>Professional Agents</h1><p>Specialized agents with practical skills, workflows and acceptance criteria.</p><p><small>Choose the role that fits your assignment and load its associated skill.</small></p>
<label for="q">Profession, related title or identifier</label><br><input id="q" placeholder="Developer, M1805, metrology…"><label for="b">Domain</label><select id="b"><option value="">All domains</option></select><div id="count" role="status"></div><table><thead><tr><th>Identifier</th><th>Profession</th><th>Files</th><th>Domain</th></tr></thead><tbody id="rows"></tbody></table>
<script>const data=""" + payload + """;const q=document.getElementById('q'),b=document.getElementById('b'),rows=document.getElementById('rows');
const norm=s=>s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();
for(const id of [...new Set(data.map(r=>r.domain))].sort()){const o=document.createElement('option');o.value=id;o.textContent=data.find(r=>r.domain===id).domain_title;b.append(o)}
function render(){const term=norm(q.value);const found=data.filter(r=>norm([r.code,r.title,...r.appellations].join(' ')).includes(term)&&(!b.value||r.domain===b.value));rows.replaceChildren();document.getElementById('count').textContent=found.length+' professions of '+data.length;for(const r of found.slice(0,250)){const tr=document.createElement('tr');for(const text of [r.code,r.title]){const td=document.createElement('td');td.textContent=text;tr.append(td)}const files=document.createElement('td');for(const [label,path] of [['Agent',r.agent],['Skill',r.skill]]){const a=document.createElement('a');a.href=path;a.textContent=label;files.append(a,document.createTextNode('  '))}tr.append(files);const td=document.createElement('td');td.textContent=r.domain_title;tr.append(td);rows.append(tr)}if(found.length>250){const tr=document.createElement('tr'),td=document.createElement('td');td.colSpan=4;td.textContent='Showing the first 250 matches; refine the search.';tr.append(td);rows.append(tr)}}q.addEventListener('input',render);b.addEventListener('change',render);render();</script></html>""")
    print(json.dumps(coverage, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
