"""Check all native profession agents, companion skills and upstream preservation."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EXTENSION = ROOT / "extensions/professions"
sys.path.insert(0, str(EXTENSION / "scripts"))
from library import runtime_issues


def main():
    index = json.loads((EXTENSION / "native-index.json").read_text(encoding="utf-8"))
    errors, names = [], set()
    for row in index:
        path = ROOT / row["agent"]
        body = path.read_text(encoding="utf-8")
        header = re.match(r"^---\n(.*?)\n---\n", body, re.S)
        if not header or any(not re.search(r"^" + field + r":\s*\S", header[1], re.M) for field in ["name", "description", "color"]):
            errors.append("Invalid native frontmatter: " + str(path.relative_to(ROOT)))
        if row["name"] in names:
            errors.append("Duplicate native agent name: " + row["name"])
        names.add(row["name"])
        errors.extend(runtime_issues([path]))
        if re.search(r"\]\((?!https?://)[^)]+\)", body):
            errors.append("Native agent has a non-portable relative link: " + row["agent"])
        if not (ROOT / row["skill"]).is_file():
            errors.append("Missing companion skill: " + row["skill"])
    if len(index) != 1923:
        errors.append("Incomplete profession coverage")
    native = list((ROOT / "professions").glob("*/*.md"))
    if len(native) != len(index):
        errors.append("Native division and index disagree")
    divisions = json.loads((ROOT / "divisions.json").read_text(encoding="utf-8"))["divisions"]
    upstream_dirs = set(divisions) - {"professions"}
    original_count = 0
    tree = subprocess.check_output(["git", "ls-tree", "-r", "HEAD"], cwd=ROOT, text=True)
    for line in tree.splitlines():
        metadata, name = line.split("\t", 1)
        if name.split("/")[0] not in upstream_dirs or not name.endswith(".md"):
            continue
        path = ROOT / name
        content = path.read_bytes()
        if not content.startswith(b"---"):
            continue
        digest = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
        if digest != metadata.split()[2]:
            errors.append("Upstream agent changed: " + name)
        original_count += 1
    report = {"status": "passed" if not errors else "failed", "upstream_agents_preserved": original_count,
              "native_profession_agents": len(native), "companion_skills": len(index), "errors": errors}
    (EXTENSION / "integration-validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
