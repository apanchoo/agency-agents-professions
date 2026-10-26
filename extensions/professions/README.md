# Professional Agent Library

A collection of **1,923 profession agents and 1,923 companion skills**, with practical methods, deliverables and acceptance criteria.

- Browse the [interactive catalog](catalog.html) or [Markdown catalog](CATALOG.md).
- Example: [Software Developer](agents/software-developer-m1805/AGENTS.md) and its [skill](skills/software-developer-m1805/SKILL.md).
- Read the [validation report](validation.json) and [coverage report](coverage.json).

## Runtime layout

```text
agents/software-developer-m1805/AGENTS.md
skills/software-developer-m1805/
    SKILL.md
    references/expertise.md
    references/practice.md
```

Folders use English profession names with a stable identifier. Runtime files incorporate professional expertise directly. They do not mention the reference materials used to construct the profiles or link to the audit records.

Each skill contains the complete activity and knowledge coverage for its role, practical methods and selected validation scenarios. Physical observations, simulations and proposed work are distinguished from completed work.

## Find and export a role

```bash
python -X utf8 scripts/library.py search "software developer"
python -X utf8 scripts/library.py export M1805 --destination exports/software-developer
```

An export contains the profile, its complete skill and a separate audit directory. Existing export destinations are never overwritten. No agents are started and no global configuration is changed.

## Construction and traceability

The library was built from France Travail's ROME 4.0 version 62, published on 19 October 2026, and the 24 national BUT curricula linked by the French ministry on 26 October 2026. The curricula contain 9,509 PDF pages; 3,600 resource or assessment records were identified. Curriculum-informed enrichment is proposed for 928 roles. The other 995 retain their professional activity and knowledge coverage.

Original materials and their hashes remain in `sources/`. Original role records, source excerpts and mapping provenance are stored under `audit/metiers/<identifier>/`. Generated English vocabulary is cached in `data/translations-en.json`; translations are machine-assisted and terminology has been reviewed on a sample, not exhaustively. Original reference documents are retained in their original language.

Mapping decisions are proposals, not official degree-to-profession equivalences. A mention of an identifier in a curriculum alone is insufficient to select a specialization. See [attribution](ATTRIBUTION.md) for source licenses and credits.

## Rebuild and validate

Python 3.10+ is required, with the dependencies in `requirements.txt`.

```bash
python -m pip install -r requirements.txt
python -X utf8 scripts/collect.py
python -X utf8 scripts/extract_programmes.py
python -X utf8 scripts/translate_library.py
python -X utf8 scripts/build_library.py
python -X utf8 scripts/library.py validate
python -X utf8 -m unittest discover -s tests -v
```

Collection and translation reuse their caches. The included source snapshot is preserved. The validator checks complete coverage, original source integrity, skill structure, readable folder names, local links, evidence for enrichment and absence of construction provenance in runtime files.

The design follows the role-oriented structure of [Agency Agents](https://github.com/msitarzewski/agency-agents): specialist identity, mission, workflow, deliverables and acceptance criteria.
