#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

from workflow_paths import project_root

ROOT = project_root()
SKILLS_ROOT = ROOT / ".agents" / "skills"
NAME_PATTERN = re.compile(r"^name:\s*([^\s].*?)\s*$", re.MULTILINE)


def extract_name(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = NAME_PATTERN.search(text)
    if not match:
        return None
    return match.group(1).strip().strip("'\"")


def main() -> int:
    if not SKILLS_ROOT.exists():
        print("SKILLS:ok")
        return 0

    by_name: dict[str, list[str]] = defaultdict(list)
    missing_name: list[str] = []

    for path in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
        name = extract_name(path)
        rel = path.relative_to(ROOT).as_posix()
        if not name:
            missing_name.append(rel)
            continue
        by_name[name].append(rel)

    errors: list[str] = []

    for rel in missing_name:
        errors.append(f"SKILLS:{rel}:missing-frontmatter-name")

    for name, rels in sorted(by_name.items()):
        if len(rels) > 1:
            errors.append(f"SKILLS:duplicate-name:{name}:{','.join(rels)}")

    if errors:
        for err in errors:
            print(err)
        return 1

    print("SKILLS:ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
