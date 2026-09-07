# Feature Inventory

> Cross-phase register of every platform capability at the current stage.
> One directory per feature; one file per subfeature.
> Behavioral truth stays in `docs/design/`. Dated progress stays in `docs/implementation/status/`.
> This tree is a rollup lens, not a source of net-new behavior.
> Spec: `spec/feature-inventory-spec.md`.

## Purpose

- Browsable list of every feature the platform offers or plans at this stage.
- Each feature is a directory; each subfeature is a small file with a description, a capability-leverage note, a status, and evidence.
- Read before planning a phase or scoping a task to see where a capability stands.

## Legend

| Status | Meaning |
|---|---|
| `Done` | Shipped and verified against acceptance criteria. |
| `In Progress` | Under active implementation; some tasks shipped, some open. |
| `In Review` | Implementation complete; awaiting verification or docs-vs-code reconciliation. |
| `Pending` | Planned and scoped; not started. |
| `Blocked` | Cannot proceed; blocker named in the subfeature file. |

## Feature Index

| # | Feature | Description | Capability leverage | Status | Link |
|---|---|---|---|---|---|
| 1 | | | | | `./<feature>/README.md` |

## Capability Outlook

- How the delivered feature set compounds into the platform's target capability.
- Named gaps between current status and best-capability usage.

## Maintenance

- Feature and subfeature split mirrors the decomposition in `docs/design/`; do not invent a different one here.
- Add a feature directory when a proposal introducing a new capability is adopted into `docs/design/`.
- Add a subfeature file when a bounded behavior is scoped in `docs/design/` or gets a backlog entry, phase line item, or task.
- Update a subfeature `Status` whenever a linked backlog entry, phase, or task changes state; re-roll the feature `Status`.
- Do not add a feature or subfeature here before its behavior exists in `docs/design/`.
- Keep feature numbers stable; never reuse a removed number.
