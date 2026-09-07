# Release Notes

## Versioning

- Git tags: `vMAJOR.MINOR.PATCH`
- Backward-incompatible changes → minor bump (pre-1.0) or major bump (post-1.0)
- Additive changes (new optional features, new scripts that don't break existing configs) → patch bump
- All releases must pass `python3 .agents/workflows/workflow-contract/scripts/validate_workflow.py` before tagging

## Consumer Upgrade Contract

1. Install by adding `git@github.com:danfordChris/workflow-doc.git` as the `.agents/workflows/workflow-contract` submodule, then run `make -C .agents/workflows/workflow-contract check`.
2. Follow the migration guide in `compatibility/migrate-vX.Y-to-vA.B.md` when present.
3. Run validator and confirm `WORKFLOW:ok`.
4. Merge only after compatibility is confirmed.

---

## Unreleased

Additive for the workflow package (`spec/`, `templates/`, `scripts/`, `repo.config.json` — no incompatible change). The companion skill is renamed and 19 vendored third-party skills are removed (see below).

### Added

- `spec/feature-inventory-spec.md` — policy for the cross-phase feature register: directory layout (`docs/implementation/feature-inventory/<feature>/<subfeature>.md`), layer rules, `Derivation` (split mirrors `docs/design/`; populated as the backlog/phases/tasks are built), required sections per file type, status vocabulary (`Done` / `In Progress` / `In Review` / `Pending` / `Blocked`), subfeature fields, update triggers keyed to backlog/phase/task creation and status changes.
- `templates/feature-inventory/` — reusable templates: inventory `README.md`, per-feature `feature-README.md`, per-subfeature `subfeature.md`.

### Changed

- `spec/workflow-spec.md` — new "Feature Inventory" section; operating-loop step 6 now names the directory register and its sync-with-planning rule.
- `scripts/validate_metadata.py` — `METADATA` validates the inventory `README.md`, every `<feature>/README.md`, and every `<feature>/<subfeature>.md` heading set **only when `docs/implementation/feature-inventory/` exists**; repos without the directory are unaffected.
- `templates/implementation-phase.md` — `Included Features` references feature-inventory subfeature files by path.
- `templates/implementation-task.md` — `Linked Phase` names the feature-inventory subfeature(s) the task delivers.
- `repo.config.json` — added `paths.implementation_feature_inventory` (directory path).
- `README.md` — package contents mention the new spec and template directory.
- `.agents/skills/workflow/SKILL.md` — canonical source #5 + a Step 3 layer-rule bullet for the feature rollup directory.

### Renamed

- Companion skill `workflow-contract-companion` → `workflow` (directory `.agents/skills/workflow-contract-companion/` → `.agents/skills/workflow/`; SKILL.md `name:`, `skills-lock.json` key, `workflow.json` `skill`, `skills.sh.json`, `agents/openai.yaml` `$workflow` trigger). Install with `npx skills add danfordChris/workflow-doc --skill workflow`. Consumers using the old `--skill workflow-contract-companion` must update the name.
- `init_workflow_contract.py` `SKILL_SOURCE` and `workflow_paths.SKILL_INSTALL_ROOT` now both resolve to `.agents/skills/workflow`. On rerun, init verifies an existing `.agents/skills/workflow/` is this skill (`SKILL.md` `name: workflow`) before skipping — an unrelated skill at that path now fails with a clear conflict instead of being silently kept.
- `make check` no longer aborts with `INIT:error:Missing source skill directory` on a fresh checkout.

### Removed

- 19 vendored third-party skills that no `spec/*` doc, kept skill, or `README.md` references: `ask-matt`, `claude-handoff`, `design-an-interface`, `edit-article`, `git-guardrails-claude-code`, `grill-me`, `loop-me`, `migrate-to-shoehorn`, `obsidian-vault`, `resolving-merge-conflicts`, `scaffold-exercises`, `setup-pre-commit`, `setup-ts-deep-modules`, `teach`, `wizard`, `writing-beats`, `writing-fragments`, `writing-great-skills`, `writing-shape`. Their `skills-lock.json` entries are dropped.
- Kept: the 16 companion skills the contract cites, the `workflow` skill, and the 4 those depend on (`grilling`, `prototype`, `improve-codebase-architecture`, `setup-matt-pocock-skills`).
- Re-add any removed skill directly from upstream if a consumer relied on it: `npx skills add mattpocock/skills --skill <name>`.

---

## v0.2.2

### Added

- `workflow.json` metadata so the public CLI can discover this workflow.
- `scripts/package_workflow_release.py` to build private `ipf-workflows-v<version>.tar.gz` release assets.
- `.agents/workflows/workflow-contract` as the canonical installed workflow location.

### Changed

- Bootstrap now uses `.agents/skills` directly and links Claude/Junie to that store.
- Bootstrap no longer creates a `GEMINI.md` bridge.
- Consumer onboarding is submodule-first via `danfordChris/workflow-doc`.

---

## v0.2.1

**Breaking changes — see `compatibility/migrate-v0.2.0-to-v0.2.1.md`.**

### Removed

- `adapters/` directory and all consumer adapter files — state does not belong in the shared library
- `adapter-template.md` — adapter concept eliminated
- `--repo-name` CLI argument from `init_workflow_contract.py` — was only used for adapter generation
- `repo_name_from_git()`, `sanitize_repo_name()`, `resolve_repo_name()`, `ensure_adapter()` from `init_workflow_contract.py`
- `.agents/workflows/workflow-contract/adapters` from `required_directories` in `repo.config.json`
- "Adapter Extension Workflow" from `CONTRIBUTING.md`
- "Adapter Name Resolution" from `repo-config-reference.md`

### Changed

- `README.md` — removed all adapter references; updated `make check` description, done checklist, AGENTS.md snippet, package contents
- `adopt-new-repo.md` — removed adapter step from bootstrap sequence and done checklist
- `CONTRIBUTING.md` — replaced adapter workflow with documentation tone rules from `spec/workflow-spec.md`
- `.agents/skills/workflow-contract/SKILL.md` — removed adapter from canonical sources and Step 2 bootstrap

### Consumer migration

Remove the `Repo adapter:` line from the `Workflow Authority` section of `AGENTS.md`:

```diff
 ## Workflow Authority

 - Canonical workflow policy: `.agents/workflows/workflow-contract/spec/*`
-- Repo adapter: `.agents/workflows/workflow-contract/adapters/<repo-name>.md`
 - Canonical validator: `python3 .agents/workflows/workflow-contract/scripts/validate_workflow.py`
```

---

## v0.2.0

**Breaking changes — see `compatibility/migrate-v0.1-to-v0.2.md`.**

### Removed

- `spec/layering-spec.md` — layer rules absorbed into `spec/workflow-spec.md`
- `spec/enforcement-spec.md` — enforcement section absorbed into `spec/guardrails-spec.md`
- `spec/glossary.md` — terms dropped (self-evident from context)

### Added

- `spec/task-spec.md` — minimum viable task standard: required sections, acceptance criteria rules, parallel agent boundary rules
- `scripts/validate_readiness.py` — `READINESS` check: in-progress tasks must have populated acceptance criteria and scope boundary; done tasks must have verification evidence
- `scripts/validate_scope_conflicts.py` — `SCOPE` check: no two in-progress tasks may claim the same scope entry
- `compatibility/migrate-v0.1-to-v0.2.md` — consumer migration guide

### Changed

- `spec/workflow-spec.md` — added agent modes (Thinking / Execution / Review), parallel agent safety rules, content style standard, layer rules (absorbed from layering-spec)
- `spec/guardrails-spec.md` — three new hard rules (no execution without acceptance criteria; no done without verification; no shared mutable scope without boundary); enforcement section absorbed from enforcement-spec
- `spec/lifecycle-spec.md` — readiness gate (planned → active) and completion gate (active → done) added and enforced by READINESS validator
- `templates/implementation-task.md` — new sections: `Agent Context`, `Scope Boundary`, `Acceptance Criteria`, `Dependencies`, `Verification`; removed `Related Design Docs`, `Verification Notes`
- `scripts/validate_metadata.py` — task files now require `Acceptance Criteria`, `Scope Boundary`, `Verification` headings
- `scripts/validate_workflow.py` — pipeline now runs 6 checks: STRUCTURE, METADATA, READINESS, SCOPE, TRANSITIONS, REFERENCES
- `repo.config.json` — added `enable_readiness`, `enable_scope_conflicts` flags; removed deleted spec files from `required_files`; added new scripts to `required_files`
- `adapter-template.md` — stale reference to `layering-spec.md` updated to `workflow-spec.md`
- `examples/task-example.md` — updated to reflect new task template
- `.agents/skills/workflow-contract/SKILL.md` — updated canonical sources, added three-way classification, task readiness table, validator failure reference
- `.agents/skills/workflow-contract/agents/openai.yaml` — expanded default prompt to reflect updated skill steps

---

## v0.1.0

Initial release.

- Three-layer doc structure: `docs/design`, `docs/implementation`, `docs/changes/proposed`
- Validator pipeline: STRUCTURE, METADATA, TRANSITIONS, REFERENCES
- Spec files: `workflow-spec.md`, `layering-spec.md`, `lifecycle-spec.md`, `guardrails-spec.md`, `enforcement-spec.md`, `glossary.md`
- Templates: design-doc, implementation-project, implementation-phase, implementation-task, implementation-status, change-proposal, decision-log-entry
