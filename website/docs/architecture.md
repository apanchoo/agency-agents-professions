---
title: Project architecture
---

# One library, two complementary perspectives

The original Agency Agents definitions are preserved. A registered `professions` division adds broader professional roles without replacing tool-specific specialists.

| Path | Purpose |
| --- | --- |
| Original division directories | Upstream specialist agents |
| `professions/` | Standalone native profession agents |
| `extensions/professions/skills/` | Companion skills and operational references |
| `extensions/professions/audit/` | Original role records and mapping evidence |
| `extensions/professions/sources/` | Source documents and integrity hashes |
| `website/` | Docusaurus, Chakra UI landing page and searchable explorer |

## Reproducible generation

The professional corpus was constructed from public occupational records and national curricula. Original documents and attribution remain in maintenance data; their construction history is absent from operational instructions. English translations are machine-assisted, with terminology reviewed on a sample.

The catalog is generated from repository files during each site build. Full documents are loaded on demand; no backend, account or third-party search service is needed.

## Upstream compatibility

The new division is registered with the existing converters, installer and structural checks. Native agent names retain stable identifiers to prevent collisions after translation or slug normalization.
