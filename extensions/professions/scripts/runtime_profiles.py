"""Profils opérationnels : compétences intégrées, sans exposer leur provenance."""
import json
import re
import unicodedata

from editorial import recipe_for
from english import tr


def folder_name(code, title):
    # Callers may already hold the translated display name.
    from english import OVERRIDES
    value = title if title in OVERRIDES.values() else tr(title)
    value = "".join(c for c in unicodedata.normalize("NFKD", value.lower()) if not unicodedata.combining(c))
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    if len(value) > 54:
        value = value[:55].rsplit("-", 1)[0]
    return f"{value}-{code.lower()}"


def neutral_text(text):
    text = tr(text)
    text = re.sub(r"France Travail|P[oô]le[- ]emploi|France Work|Employment Center", "public employment service", text, flags=re.I)
    text = re.sub(r"\bROME\b(?:\s*4\.0)?", "professional", text)
    return text


def bullet(values):
    return "\n".join("- " + str(v).replace("\n", " ") for v in values)


def items(fiche, category):
    groups = fiche.get("competences", {}).get(category, {})
    return [item for group in groups.get("enjeux", groups.get("categories", [])) for item in group.get("items", [])]


def core_activities(fiche):
    values = items(fiche, "savoir_faire")
    return ([c for c in values if c.get("coeur_metier")] + [c for c in values if not c.get("coeur_metier")])[:8]


def practice_content(matches, steps, outputs, checks):
    # Intégrer les domaines techniques et les mises en situation au langage du
    # métier, sans charger les pages originales ni leurs métadonnées scolaires.
    topics, scenarios = [], []
    for match in matches:
        for module in match["modules"]:
            target = scenarios if module["kind"] == "sae" else topics
            title = neutral_text(module["title"])
            if title not in target:
                target.append(title)
    blocks = ["# Methods and Validation", "## Workflow\n\n" + "\n".join(f"{i}. {tr(step)}." for i, step in enumerate(steps, 1))]
    if topics:
        blocks.append("## Technical Areas\n\nSelect techniques that fit the task and available resources.\n\n" + bullet(topics))
    if scenarios:
        blocks.append("## Validation Scenarios\n\nChoose a scenario suited to the deliverable and specify inputs, constraints, expected results and checks.\n\n" + bullet(scenarios))
    blocks += ["## Deliverables\n\n" + bullet(tr(v) for v in outputs), "## Acceptance Criteria\n\n" + bullet(tr(v) for v in checks),
               "Retain assumptions, units, inputs and intermediate results needed to reproduce the checks. Distinguish observed results from checks that still need to be performed."]
    return "\n\n".join(blocks)


def expertise_content(fiche):
    blocks = [f"# {tr(fiche['rome']['intitule'])}", "## Scope\n\n" + neutral_text(fiche["definition"]),
              "## Related Job Titles\n\n" + bullet(neutral_text(a["libelle"]) for a in fiche.get("appellations", []))]
    for key, label in [("savoir_faire", "Activities and Skills"), ("savoir_etre_professionnel", "Professional Approach")]:
        blocks.append(f"## {label}\n\n" + bullet(neutral_text(c["libelle"]) for c in items(fiche, key)))
    groups = fiche.get("competences", {}).get("savoirs", {}).get("categories", [])
    for group in groups:
        if group["libelle"] == "Certifications et habilitations":
            continue
        blocks.append("## " + tr(group["libelle"]) + "\n\n" + bullet(neutral_text(c["libelle"]) for c in group.get("items", [])))
    blocks.append("## Working Conditions\n\n" + bullet(neutral_text(i["libelle"]) for g in fiche.get("contextes_travail", []) for i in g.get("items", [])))
    blocks.append("## Sectors\n\n" + bullet(neutral_text(x["libelle"]) for x in fiche.get("secteurs_activite", [])))
    return "\n\n".join(blocks)


def generate_profile(fiche, meta, source, matches):
    code, title = fiche["rome"]["code_rome"], tr(fiche["rome"]["intitule"])
    name = folder_name(code, fiche["rome"]["intitule"])
    core = bullet(neutral_text(c["libelle"]) for c in core_activities(fiche))
    behaviour = bullet(neutral_text(c["libelle"]) for c in items(fiche, "savoir_etre_professionnel"))
    steps, outputs, checks = recipe_for(code, matches[0]["programme_id"] if matches else None)
    scope = (f"You are a specialist assistant working as a {title}. Analyze requirements, prepare interventions "
             "and produce usable deliverables. Explain decisions precisely and adapt your work to the assignment. "
             "Distinguish completed work, simulations and physical operations still to be performed. "
             "Do not claim personal experience, qualifications or credentials you do not possess.")
    if meta.get("emploi_reglemente") == "O":
        scope += " Identify actions that require validation by an authorized professional."
    if code.startswith("J"):
        scope += " Identify situations that require assessment by a healthcare professional."
    definition = neutral_text(fiche["definition"])
    method = "\n".join(f"{i}. {tr(step)}." for i, step in enumerate(steps, 1))
    agent = f"""# {title}

## Role and Mission

{scope}

{definition}

## Working Style

{behaviour or '- Explain decisions and adapt the level of detail to the recipient.'}

## Core Skills

{core}

Consult the [detailed expertise](../../skills/{name}/references/expertise.md) to adapt the work to the assignment.

## Workflow

{method}

Select activities relevant to the assignment and the evidence needed to assess the outcome.

## Deliverables

{bullet(tr(v) for v in outputs)}

## Acceptance Criteria

{bullet(tr(v) for v in checks)}

For each selected activity, specify the expected outcome, available evidence and outstanding checks. Do not declare a check successful without an observed result.

Consult the [methods and validation scenarios](../../skills/{name}/references/practice.md) for the relevant techniques.

## Execution

Use the [associated skill](../../skills/{name}/SKILL.md) to carry out the assignment with its acceptance criteria.
"""
    skill = f"""---
name: {name}
description: {json.dumps(f'Prepare, analyze and produce deliverables as a {title}; use for requests within this professional scope.', ensure_ascii=False)}
---

# {title}

{scope}

## Scope

{definition}

Check that the request fits the required skills and expected outcome. Consult the [activities, knowledge and working contexts](references/expertise.md) as needed.

## Skills to Apply

{core}

## Execution

{method}

Review the techniques and choose a validation scenario in the [practical methods](references/practice.md). Retain assumptions, units, inputs and intermediate results needed to verify the deliverable.

## Expected Deliverables

{bullet(tr(v) for v in outputs)}

## Validation

{bullet(tr(v) for v in checks)}

Deliver a usable result with available evidence and known limitations. Distinguish completed work from checks that have only been planned.
"""
    return agent, skill
