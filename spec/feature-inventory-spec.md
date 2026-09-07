# Feature Inventory Spec

## Objective

Maintain a cross-phase register of every platform capability: what it is, how it advances the platform toward its best-capability usage, and its current delivery status. The register is a directory tree so each feature is browsable on its own and subfeatures are small enough to build one at a time.

## Location

- Single directory: `docs/implementation/feature-inventory/`.
- One per repo. Do not fragment it per service or per phase.
- Layout:

```
docs/implementation/feature-inventory/
  README.md              # inventory index: purpose, legend, feature index, capability outlook, maintenance
  <feature>/             # one directory per feature (e.g. auth, booking, selling)
    README.md            # feature rollup: description, capability leverage, rolled-up status, subfeature index
    <subfeature>.md      # one file per subfeature (e.g. login, password-reset)
```

- Feature directory name: kebab-case capability name as used in `docs/design/`.
- Subfeature file name: kebab-case, one bounded behavior per file.
- Created from `templates/feature-inventory/`.

## Layer Rules

- The inventory is an execution-planning rollup. It lives in `docs/implementation/`.
- It references behavior; it does not define it. Every subfeature file traces to a `docs/design/` doc (or an accepted proposal).
- It references progress; it does not replace `docs/implementation/status/`. Status here is a current-state rollup, not a dated log.
- No feature directory or subfeature file introduces scope absent from `docs/design/`.
- Deferred / out-of-scope capabilities are listed only when `docs/design/` names them as deferred.

## Derivation

- The feature / subfeature split mirrors how the originating idea is decomposed in `docs/design/`. Do not invent a different decomposition here.
- One feature directory per capability named in design. One subfeature file per bounded behavior that will get its own backlog entry, phase line item, or task.
- The inventory is populated as planning proceeds: adopting a proposal creates feature directories and `Pending` subfeature files; breaking work into a backlog and phases fills in evidence links; execution and review move statuses.
- Backlog entries, phase `Included Features`, and task `Linked Phase` reference subfeature files by path. They do not restate the description or capability-leverage note.
- If planning produces a behavior with no matching subfeature file, add the file — do not let the backlog carry scope the inventory does not show.

## Required Sections

### `README.md` (inventory index)

| Heading | Content |
|---|---|
| `Purpose` | Why the register exists; when to read it. |
| `Legend` | Status vocabulary table. |
| `Feature Index` | One row per feature directory: number, name, description, capability leverage, rolled-up status, link to `<feature>/README.md`. |
| `Capability Outlook` | How the feature set compounds toward best-capability usage; named gaps between current status and that target. |
| `Maintenance` | Rules for keeping directories, rows, and statuses current. |

### `<feature>/README.md` (feature rollup)

| Heading | Content |
|---|---|
| `Feature` | Capability name as used in `docs/design/`. |
| `Description` | One or two sentences: what the feature does for a user or the system. |
| `Capability Leverage` | One sentence: what this feature unlocks or compounds. |
| `Status` | Rolled-up value from the vocabulary below (worst active subfeature state; `Blocked` if any subfeature is blocked). |
| `Subfeature Index` | One row per subfeature file: name, description, status, evidence. |

### `<feature>/<subfeature>.md` (subfeature)

| Heading | Content |
|---|---|
| `Description` | One or two sentences: what this bounded behavior does. |
| `Capability Leverage` | One sentence: what it unlocks or compounds. |
| `Status` | One value from the vocabulary below. |
| `Evidence` | Link to the design doc, plus the backlog entry and phase/task IDs that deliver it. |

Enforced by the `METADATA` validator check when `docs/implementation/feature-inventory/` exists.

## Subfeature File Fields

| Field | Rule |
|---|---|
| `Description` | One or two sentences: what the subfeature does for a user or the system. |
| `Capability Leverage` | One sentence: what this subfeature unlocks or compounds — how it pushes the platform to its best use. |
| `Status` | One value from the vocabulary below. |
| `Evidence` | Link to the design doc, plus the backlog entry and phase/task IDs that deliver it. |

## Status Vocabulary

| Status | Enter when | Leave when |
|---|---|---|
| `Pending` | Subfeature scoped in design and planned in a phase. | First implementing task moves to `in-progress`. |
| `In Progress` | Any implementing task is `in-progress`, or some implementing tasks are `done` and others open. | All implementing tasks are `done`. |
| `In Review` | All implementing tasks `done`; acceptance criteria or docs-vs-code reconciliation not yet confirmed. | Acceptance verified against the linked design/phase doc. |
| `Done` | Acceptance criteria in the linked design/phase doc verified with evidence. | Scope changes and new tasks open. |
| `Blocked` | A named dependency prevents progress. | Blocker cleared; row returns to its prior status. |

## Update Triggers

- A proposal is adopted into `docs/design/` → add a subfeature file (`Pending`), and a feature directory if the capability is new.
- A backlog entry, phase, or task is created for a behavior → ensure its subfeature file exists and add the entry/ID to `Evidence`.
- A linked backlog entry, phase, or task changes status → update the subfeature `Status` and re-roll the feature `Status`.
- A phase acceptance pass completes → promote its subfeatures to `Done`.
- A review / reconciliation pass finds drift → correct the file and note it in `docs/implementation/status/`.
- A behavior is removed from `docs/design/` → mark its subfeature file removed and stop counting it in the rollup; keep the feature number stable.

## Validation

- `python3 scripts/validate_workflow.py` — `METADATA` checks the required sections in `README.md`, every `<feature>/README.md`, and every `<feature>/<subfeature>.md` when `docs/implementation/feature-inventory/` exists.
- Review gate: every subfeature file has a non-empty description, capability-leverage note, status from the vocabulary, and an evidence link; every feature `README.md` rolls up its subfeature statuses.
