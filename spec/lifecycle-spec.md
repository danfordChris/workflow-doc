# Lifecycle Spec

## States

1. Idea
2. Wayfinding
3. Proposed
4. Adopted in design
5. Planned in implementation
6. Active implementation
7. Reported status
8. Reconciled completion

## State Movement

- **Idea → Wayfinding**: create a wayfinding map when the route is unclear or too large for one session.
- **Idea → Proposed**: create or update proposal doc in `docs/changes/proposed` when the unresolved change is already concrete.
- **Wayfinding → Proposed**: convert resolved decision-map output into one or more concrete proposals when behavior is now specifiable.
- **Proposed → Adopted**: merge accepted behavior into `docs/design`. Remove from proposed.
- **Adopted → Planned**: update `docs/implementation/project` and phase/task docs.
- **Planned → Active**: task must pass readiness gate before status moves to `in-progress`.
- **Active → Reported**: reflect delivery state in `docs/implementation/status`.
- **Reported → Reconciled**: task must pass completion gate. Ensure design and implementation remain aligned.

## Readiness Gate

A task cannot move to `in-progress` until:

- `Acceptance Criteria` is populated with at least one binary, verifiable condition.
- `Scope Boundary` explicitly states what is in scope and what is out of scope.
- `Agent Context` names the design docs and skills the executing agent must read first.
- `Session Budget` states mode, stop conditions, and handoff trigger.

Enforced by the `READINESS` validator check.

## Completion Gate

A task cannot move to `done` until:

- `Verification` contains command output, test results, or explicit reconciliation evidence — not a placeholder.
- Review notes cover both standards and spec correctness, whether in one review doc or linked review artifacts.

Enforced by the `READINESS` validator check.
