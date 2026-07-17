# Adopt in New Repo

Use this sequence when onboarding `.agents/workflows/workflow-contract` into a different repository.

## Prerequisites

- Python 3 available in CI and local development.
- Docs root in the consumer repo at `docs/`.

## Bootstrap Sequence

Plain `agents-setup init` only creates agent wiring and does not create `docs/`. Use the workflow setup when this workflow contract should own the repo docs scaffold.

1. Run the public no-clone setup CLI:
   ```bash
   npx @jerrylusato/agents-setup init --workflow workflow-contract --yes
   ```
2. Run validation when you need an explicit check:
   ```bash
   make -C .agents/workflows/workflow-contract check
   ```
3. Add the required snippet below to `AGENTS.md`.
4. Tune `.agents/workflows/workflow-contract/repo.config.json` for your repo paths and constraints.

`make check` does not edit an existing `AGENTS.md`. Add the snippet manually so repo-specific agent instructions stay intentional.

Manual fallback:

```bash
git submodule add git@github.com:danfordChris/workflow-doc.git .agents/workflows/workflow-contract
git submodule update --init --recursive
make -C .agents/workflows/workflow-contract check
```

Done when:

- `AGENTS.md` contains `Workflow Authority` and `Start Here`.
- `.agents/workflows/workflow-contract/repo.config.json` has the correct repo name.
- `python3 .agents/workflows/workflow-contract/scripts/validate_workflow.py` ends with `WORKFLOW:ok`.

## Manual Fallback (No Make)

```bash
python3 .agents/workflows/workflow-contract/scripts/init_workflow_contract.py
python3 .agents/workflows/workflow-contract/scripts/validate_workflow.py
```

## Required AGENTS.md Snippet

```md
## Workflow Authority

- Canonical workflow policy: `.agents/workflows/workflow-contract/spec/*`
- Canonical validator: `python3 .agents/workflows/workflow-contract/scripts/validate_workflow.py`

## Start Here

1. Classify the task.
2. Run `python3 .agents/workflows/workflow-contract/scripts/validate_workflow.py`.
3. Read `docs/design/`.
4. Read `docs/implementation/`.
5. If the effort is large and foggy, read or create `docs/changes/wayfinding/`.
6. If behavior is unresolved but already concrete, read or create `docs/changes/proposed/`.
7. Load required repo skill(s).
8. Inspect target service code before editing.
```

## Optional AGENTS.md Reinforcement

```md
## Documentation Workflow

Use `$workflow-contract` for:

- design docs
- implementation docs
- wayfinding maps
- backlog, phase, task, and status updates
- proposed changes
- docs-vs-code reconciliation
- workflow validation failures

Layer rules:

- `docs/design/`: approved product/system truth.
- `docs/implementation/`: execution plans, phases, tasks, and status only.
- `docs/changes/wayfinding/`: unresolved decision maps for large efforts only.
- `docs/changes/proposed/`: unresolved proposals only.

Do not define net-new behavior in implementation docs. Put unresolved behavior in `docs/changes/proposed` until accepted.
```

## Recommended Companion Skills

Install companion skills only if you want stronger operator guidance around the contract.

- Use `wayfinder` for large unclear efforts before writing a proposal or spec.
- Use `research` to gather primary-source facts into a durable note before approving design truth.
- Use `to-spec` only after discovery is sufficiently sharp that the work is no longer in wayfinding.
- Use `to-tickets` after design approval to break work into vertical slices with explicit blockers.
- Use `implement` and `tdd` only for tasks that already pass the readiness gate.
- Use `diagnosing-bugs` for defect work; require a red-capable loop before code changes.
- Use `code-review`, `qa`, and `handoff` during review and reconciliation.
- Start with these as recommended operating guidance. Promote any rule to validator enforcement only after local trial data justifies it.

If an imported skill duplicates a workflow skill name, keep this workflow contract authoritative until you intentionally merge and review the difference.

## Non-Mutating Dry-Run Checklist

- Each bootstrap step has an explicit input and output path.
- No step depends on undocumented repo-specific behavior.
- Read order is clear: `docs/design` → `docs/implementation` → `docs/changes/wayfinding` → `docs/changes/proposed`.
- No circular references between onboarding docs.
- Validator command and expected output are present in onboarding docs.
- `AGENTS.md` has workflow authority and startup order.
