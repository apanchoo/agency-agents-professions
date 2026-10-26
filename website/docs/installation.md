---
title: Installation and use
---

# Use the library

Clone the repository, choose the agents relevant to your task and keep the full associated skill folders.

```bash
git clone https://github.com/apanchoo/agency-agents-professions.git
cd agency-agents-professions
./scripts/convert.sh --tool codex
./scripts/install.sh --tool codex --division professions --agent profession-software-developer-m1805
```

The upstream installer supports several tools. Read the integration guide for your chosen environment before installing.

## Companion skills

The Software Developer skill is in `extensions/professions/skills/software-developer-m1805/`. Copy that complete directory to the skill location supported by your tool. Its references contain practical expertise and methods.

## Export a profession

```bash
python extensions/professions/scripts/library.py search "software developer"
python extensions/professions/scripts/library.py export M1805 --destination ./exports/software-developer
```

Exports include a separate audit directory for maintainers. Operational instructions do not refer to construction materials.
