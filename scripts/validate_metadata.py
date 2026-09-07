#!/usr/bin/env python3
from __future__ import annotations

import sys
import json
import re
from pathlib import Path

from workflow_paths import config_path, project_root

ROOT = project_root()
CONFIG_PATH = config_path()


def load_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def has_heading(text: str, heading: str) -> bool:
    pattern = rf"^##\s+{re.escape(heading)}\s*$"
    return re.search(pattern, text, flags=re.MULTILINE) is not None


def has_any_heading(text: str, headings: list[str]) -> bool:
    return any(has_heading(text, heading) for heading in headings)


def main() -> int:
    config = load_config()
    enabled = bool(config.get("validation", {}).get("enable_metadata", False))
    if not enabled:
        print("METADATA:skipped")
        return 0

    errors: list[str] = []

    proposal_dir = ROOT / config["paths"]["changes_proposed"]
    wayfinding_maps_dir = ROOT / config["paths"]["changes_wayfinding_maps"]
    wayfinding_tickets_dir = ROOT / config["paths"]["changes_wayfinding_tickets"]
    phase_dir = ROOT / config["paths"]["implementation_phases"]
    task_dir = ROOT / config["paths"]["implementation_tasks"]
    review_dir = ROOT / config["paths"]["implementation_reviews"]
    project_path = ROOT / config["paths"]["implementation_project"]
    status_path = ROOT / config["paths"]["implementation_status"] / "weekly-status.md"

    for path in sorted(wayfinding_maps_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        required = ["Destination", "Known Facts", "Decision Queue", "Frontier", "Out of Scope", "Exit Criteria"]
        missing = [h for h in required if not has_heading(text, h)]
        if missing:
            rel = path.relative_to(ROOT).as_posix()
            errors.append(f"METADATA:{rel}:missing-sections:{','.join(missing)}")

    for path in sorted(wayfinding_tickets_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        required = ["Status", "Question", "Type", "Inputs", "Method", "Resolution", "Next Unlocks"]
        missing = [h for h in required if not has_heading(text, h)]
        if missing:
            rel = path.relative_to(ROOT).as_posix()
            errors.append(f"METADATA:{rel}:missing-sections:{','.join(missing)}")

    for path in sorted(proposal_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        required = ["Status", "Context", "Problem"]
        missing = [h for h in required if not has_heading(text, h)]
        if not has_any_heading(text, ["Proposed Change", "Proposed Boundary"]):
            missing.append("Proposed Change|Proposed Boundary")
        if missing:
            rel = path.relative_to(ROOT).as_posix()
            errors.append(f"METADATA:{rel}:missing-sections:{','.join(missing)}")

    for path in sorted(phase_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        missing: list[str] = []
        if not has_heading(text, "Scope"):
            missing.append("Scope")
        if not has_any_heading(text, ["Features", "Included Features"]):
            missing.append("Features|Included Features")
        if not has_any_heading(text, ["Tasks", "Task Checklist"]):
            missing.append("Tasks|Task Checklist")
        if not has_heading(text, "Acceptance Criteria"):
            missing.append("Acceptance Criteria")
        if missing:
            rel = path.relative_to(ROOT).as_posix()
            errors.append(f"METADATA:{rel}:missing-sections:{','.join(missing)}")

    for path in sorted(task_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if path.name == "backlog.md":
            required = ["Status", "Objective", "Implementation Checklist"]
            missing = [h for h in required if not has_heading(text, h)]
        else:
            required = ["Status", "Acceptance Criteria", "Scope Boundary", "Session Budget", "Verification"]
            missing = [h for h in required if not has_heading(text, h)]
            if not has_any_heading(text, ["Objective", "Goal"]):
                missing.append("Objective|Goal")
        if missing:
            rel = path.relative_to(ROOT).as_posix()
            errors.append(f"METADATA:{rel}:missing-sections:{','.join(missing)}")

    for path in sorted(review_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        required = ["Summary", "Standards", "Spec", "Verification", "Follow-ups"]
        missing = [h for h in required if not has_heading(text, h)]
        if missing:
            rel = path.relative_to(ROOT).as_posix()
            errors.append(f"METADATA:{rel}:missing-sections:{','.join(missing)}")

    project_text = project_path.read_text(encoding="utf-8", errors="ignore")
    project_required = ["Overview", "Current Priorities", "Active Phases", "Linked Artifacts"]
    project_missing = [h for h in project_required if not has_heading(project_text, h)]
    if project_missing:
        rel = project_path.relative_to(ROOT).as_posix()
        errors.append(f"METADATA:{rel}:missing-sections:{','.join(project_missing)}")

    feature_inventory_rel = config["paths"].get(
        "implementation_feature_inventory", "docs/implementation/feature-inventory"
    )
    feature_inventory_path = ROOT / feature_inventory_rel
    if feature_inventory_path.is_dir():
        index_path = feature_inventory_path / "README.md"
        if not index_path.is_file():
            errors.append(f"METADATA:{feature_inventory_rel}/README.md:missing-file")
        else:
            fi_text = index_path.read_text(encoding="utf-8", errors="ignore")
            fi_required = ["Purpose", "Legend", "Feature Index", "Capability Outlook", "Maintenance"]
            fi_missing = [h for h in fi_required if not has_heading(fi_text, h)]
            if fi_missing:
                errors.append(
                    f"METADATA:{feature_inventory_rel}/README.md:missing-sections:{','.join(fi_missing)}"
                )
        for feature_dir in sorted(p for p in feature_inventory_path.iterdir() if p.is_dir()):
            feature_rel = feature_dir.relative_to(ROOT).as_posix()
            feature_readme = feature_dir / "README.md"
            if not feature_readme.is_file():
                errors.append(f"METADATA:{feature_rel}/README.md:missing-file")
            else:
                fr_text = feature_readme.read_text(encoding="utf-8", errors="ignore")
                fr_required = ["Feature", "Description", "Capability Leverage", "Status", "Subfeature Index"]
                fr_missing = [h for h in fr_required if not has_heading(fr_text, h)]
                if fr_missing:
                    errors.append(
                        f"METADATA:{feature_rel}/README.md:missing-sections:{','.join(fr_missing)}"
                    )
            subfeature_files = sorted(
                p for p in feature_dir.glob("*.md") if p.name != "README.md"
            )
            if not subfeature_files:
                errors.append(f"METADATA:{feature_rel}:no-subfeature-files")
            for sub in subfeature_files:
                sub_rel = sub.relative_to(ROOT).as_posix()
                sub_text = sub.read_text(encoding="utf-8", errors="ignore")
                sub_required = ["Description", "Capability Leverage", "Status", "Evidence"]
                sub_missing = [h for h in sub_required if not has_heading(sub_text, h)]
                if sub_missing:
                    errors.append(
                        f"METADATA:{sub_rel}:missing-sections:{','.join(sub_missing)}"
                    )

    status_text = status_path.read_text(encoding="utf-8", errors="ignore")
    if not re.search(r"^##\s+\d{4}-\d{2}-\d{2}", status_text, re.MULTILINE):
        rel = status_path.relative_to(ROOT).as_posix()
        errors.append(f"METADATA:{rel}:missing-date-status-headings")

    if errors:
        for err in errors:
            print(err)
        return 1

    print("METADATA:ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
