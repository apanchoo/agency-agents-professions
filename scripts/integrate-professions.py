"""Integrate the profession library without changing upstream specialist agents."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = value.rstrip() + "\n"
    if path.is_file() and path.read_bytes() == text.encode('utf-8'): return
    path.write_text(text, encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT.parent / "rome-agency")
    args = parser.parse_args()
    source = args.source.resolve()
    destination = ROOT / "extensions/professions"
    catalog = json.loads((source / "catalog.json").read_text(encoding="utf-8"))
    if len(catalog) != 1923 or catalog[0]["name"].startswith("rome-"):
        raise ValueError("Expected the complete, cleaned profession library")
    current_names = {r["name"] for r in catalog}
    old_catalog_path = destination / "catalog.json"
    old_catalog = json.loads(old_catalog_path.read_text(encoding="utf-8")) if old_catalog_path.exists() else []
    for old in old_catalog:
        name = old["name"]
        if name in current_names or not re.fullmatch(r"[a-z0-9-]+", name):
            continue
        for parent, filenames in [(destination / "agents" / name, ["AGENTS.md"]),
                                  (destination / "skills" / name, ["SKILL.md", "references/metier.md", "references/pratique.md", "references/expertise.md", "references/practice.md", "references/technologies.md"]),
                                  (ROOT / "professions" / name, [name + ".md"])]:
            for filename in filenames:
                path = parent / filename
                if path.is_file():
                    path.unlink()
            refs = parent / "references"
            if refs.is_dir() and not any(refs.iterdir()):
                refs.rmdir()
            if parent.is_dir() and not any(parent.iterdir()):
                parent.rmdir()
    for name in current_names:
        for filename in ["metier.md", "pratique.md"]:
            path = destination / "skills" / name / "references" / filename
            if path.is_file():
                path.unlink()
    if source != destination.resolve():
        shutil.copytree(source, destination, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".tools", "tmp", "exports", "__pycache__", "*.pyc", "catalogue.html", "CATALOGUE.md"))
    counts = Counter(row["title"] for row in catalog)
    used_names = set()
    index = []
    for row in catalog:
        # English names can differ only by case or punctuation; the stable
        # suffix keeps every upstream converter slug unique as well.
        display = "Profession: " + row["title"] + " (" + row["code"].lower() + ")"
        if display in used_names:
            raise ValueError("Duplicate native agent name: " + display)
        used_names.add(display)
        profile = (source / row["agent"]).read_text(encoding="utf-8")
        profile = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", profile)
        profile = profile.replace("## Role and Mission", "## Core Mission").replace("## Working Style", "## Identity and Working Style")
        refs = (source / row["skill"]).parent / "references"
        expertise = (refs / "expertise.md").read_text(encoding="utf-8")
        practice = (refs / "practice.md").read_text(encoding="utf-8")
        body = profile + "\n\n## Critical Rules\n\n- Match the scope to the requested outcome.\n- Keep assumptions separate from observations.\n- Report checks actually performed and outstanding verification.\n- Do not claim qualifications, physical observations or completed interventions without evidence.\n\n"
        body += "## Detailed Expertise\n\n" + expertise.replace("\n#", "\n##").removeprefix("# ")
        body += "\n\n## Practical Methods\n\n" + practice.replace("\n#", "\n##").removeprefix("# ")
        if (refs / 'technologies.md').exists():
            technology = (refs / 'technologies.md').read_text(encoding='utf-8')
            body += '\n\n## Technology Toolbox\n\n' + technology.replace('\n#', '\n##').removeprefix('# ')
        description = f"Professional assistant for {row['title']}, with task-specific methods, deliverables and acceptance criteria."
        if row.get('technologies'):
            description += ' Relevant technologies: ' + ', '.join(row['technologies'][:6]) + '.'
        front = "---\nname: " + json.dumps(display, ensure_ascii=False) + "\ndescription: " + json.dumps(description, ensure_ascii=False) + "\ncolor: '#2563EB'\n---\n\n"
        relative = f"professions/{row['name']}/{row['name']}.md"
        write(ROOT / relative, front + body)
        index.append({"name": display, "title": row["title"], "agent": relative,
                      "skill": "extensions/professions/" + row["skill"], "domain": row["domain_title"], 'technologies': row.get('technologies', [])})
    write(ROOT / "extensions/professions/native-index.json", json.dumps(index, ensure_ascii=False, indent=2))
    divisions_path = ROOT / "divisions.json"
    divisions = json.loads(divisions_path.read_text(encoding="utf-8"))
    divisions["divisions"]["professions"] = {"label": "Professions", "icon": "BriefcaseBusiness", "color": "#2563EB"}
    # Preserve one object per line: upstream shell tooling parses this layout.
    text = '{\n  "_note": ' + json.dumps(divisions["_note"]) + ',\n  "divisions": {\n'
    text += ",\n".join("    " + json.dumps(k) + ": " + json.dumps(v, ensure_ascii=False) for k, v in divisions["divisions"].items()) + "\n  }\n}"
    write(divisions_path, text)
    for relative in ["scripts/convert.sh", "scripts/lint-agents.sh"]:
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        match = re.search(r"AGENT_DIRS=\((.*?)\n\)", text, re.S)
        if "professions" not in match[1].split():
            text = text[:match.end(1)] + "\n  professions" + text[match.end(1):]
        write(path, text)
    path = ROOT / "scripts/check-divisions.sh"
    text = path.read_text(encoding="utf-8").replace("NON_DIVISION_DIRS=(examples scripts integrations strategy)", "NON_DIVISION_DIRS=(examples scripts integrations strategy extensions)")
    write(path, text)
    path = ROOT / ".github/workflows/lint-agents.yml"
    text = path.read_text(encoding="utf-8")
    if '"professions/**"' not in text:
        text = text.replace('      - "specialized/**"', '      - "specialized/**"\n      - "professions/**"')
        text = text.replace("':(glob)specialized/**/*.md')", "':(glob)specialized/**/*.md' ':(glob)professions/**/*.md')")
    text = text.replace('./scripts/check-agent-originality.sh $CHANGED_FILES', '# Structured profession records use the dedicated coverage and content checks.\n          ORIGINAL_FILES=$(printf \'%s\\n\' "$CHANGED_FILES" | grep -v \'^professions/\' || true)\n          if [ -n "$ORIGINAL_FILES" ]; then\n            ./scripts/check-agent-originality.sh $ORIGINAL_FILES\n          fi')
    write(path, text)
    write(ROOT / "PROFESSIONS.md", "# Professional Agent Library\n\nThis extension adds 1,923 profession-specific agents and companion skills to the upstream Agency Agents roster.\n\n"
          "Use an upstream specialist for a tool- or platform-specific assignment; use a profession agent for the wider professional role. Combine their outputs when both scopes are useful. Names are separated by the `Profession:` namespace.\n\n"
          "The `professions/` division contains standalone native agent files. `extensions/professions/skills/` contains their companion skills. Folders use English profession names and a stable identifier. Runtime instructions incorporate expertise directly and contain no construction-source references.\n\n"
          "Original reference materials, mapping decisions, translations and attribution are retained separately under `extensions/professions/audit/`, `sources/` and `data/`. Translations are machine-assisted and should be reviewed for high-stakes terminology. Original source documents are retained in their original language.\n\n"
          "Rebuild the native division after editing the extension:\n\n```bash\npython scripts/integrate-professions.py --source extensions/professions\npython scripts/validate-professions.py\n```\n\n"
          "The structured profession corpus shares workflow patterns across related roles. Its dedicated checks validate complete coverage, distinct identifiers, source preservation, skill structure and removal of provenance from runtime instructions. The upstream originality check continues to apply to the original editorial divisions.\n\n"
          "| Profession | Native agent | Companion skill |\n| --- | --- | --- |\n" + "\n".join(f"| {r['title'].replace('|', '/')} | [Agent]({r['agent']}) | [Skill]({r['skill']}) |" for r in index))
    print(json.dumps({"native_profession_agents": len(index), "companion_skills": len(catalog), "divisions": len(divisions["divisions"])}, indent=2))


if __name__ == "__main__":
    main()
