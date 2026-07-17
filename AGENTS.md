# AGENTS.md

## Workflow Authority

- Canonical workflow policy: `/Users/danfordchris/projects/starterpacks/workflow-contract/spec/*`
- Canonical validator: `python3 /Users/danfordchris/projects/starterpacks/workflow-contract/scripts/validate_workflow.py`

## Start Here

1. Classify the task by layer, lifecycle state, and agent mode.
2. Run `python3 /Users/danfordchris/projects/starterpacks/workflow-contract/scripts/validate_workflow.py` when changing workflow docs or templates.
3. Read `/Users/danfordchris/projects/starterpacks/workflow-contract/spec/workflow-spec.md`.
4. Use companion skills only as operator playbooks; they do not override this repo's workflow contract.

## Companion Skills

- Discovery: `wayfinder`, `research`, `grill-with-docs`, `domain-modeling`, `ubiquitous-language`
- Specification: `to-spec`, `codebase-design`
- Planning: `to-tickets`, `triage`, `request-refactor-plan`
- Execution: `implement`, `tdd`
- Review: `code-review`, `qa`, `handoff`
- Debugging: `diagnosing-bugs`

If an imported skill is also named `workflow-contract`, treat this repository's `spec/*` as authoritative unless the difference has been intentionally merged here.
