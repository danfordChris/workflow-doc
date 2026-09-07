# Workflow Spec

## Objective

Run a planning-first engineering loop that keeps documented truth synchronized with execution.

## Agent Modes

Three distinct modes. Do not conflate them.

- **Thinking**: research, constraints discovery, requirement clarification, design tradeoffs, sequencing, context preparation. Output: design docs, task definitions, acceptance criteria, scope boundaries. No code changes in this mode.
- **Execution**: implement against a prepared task artifact. Agents in this mode operate against an explicit task, scope boundary, and acceptance criteria — not open-ended prompts. Thinking must be complete before execution begins.
- **Review**: verify output matches design truth, detect drift, reconcile docs with actual state. Output: reconciliation notes, updated status, surfaced unresolved decisions.

## Operating Loop

1. Research and clarify request context. *(Thinking)*
2. If the effort is too large or foggy for one session, chart it in `docs/changes/wayfinding`. *(Thinking)*
3. Align on requirements, constraints, and acceptance criteria. *(Thinking)*
4. Record approved truth in `docs/design`. *(Thinking)*
5. Convert truth into execution plan in `docs/implementation`. *(Thinking)*
6. Break execution into phases and tasks. Each task must satisfy the task readiness standard and fit a bounded session budget. Register every capability as a directory in `docs/implementation/feature-inventory/`, broken into per-subfeature files. *(Thinking)*
7. Implement against explicit tasks and checklists. *(Execution)*
8. Review outcomes on both standards and spec correctness, then reconcile docs with actual state. *(Review)*
9. Repeat for new requirements and deltas.

## Companion Skills

Use companion skills to strengthen each phase. The workflow contract remains the source of truth. Skills help produce better artifacts; they do not change layer rules.

| Phase | Preferred skills | Use for |
|---|---|---|
| Discovery | `research`, `wayfinder`, `grill-with-docs`, `domain-modeling`, `ubiquitous-language` | Gather facts from primary sources, map foggy efforts, sharpen vocabulary, surface decisions |
| Specification | `to-spec`, `codebase-design` | Turn settled direction into a concrete design artifact without mixing execution detail into planning |
| Planning | `to-tickets`, `triage`, `request-refactor-plan` | Break approved work into vertical slices, sequence blockers, and keep tasks ready for execution |
| Execution | `implement`, `tdd` | Deliver one prepared task per session with explicit verification |
| Review | `code-review`, `qa`, `handoff` | Check behavioral correctness, capture residual risk, and reset context cheaply between sessions |
| Debugging | `diagnosing-bugs` | Build a red-capable loop before proposing fixes |

## Skill Boundaries

- This repo's canonical workflow authority is `spec/*` plus `scripts/validate_workflow.py`.
- If another installed skill is also named `workflow-contract`, do not treat it as authoritative for this repo unless its content has been intentionally merged here.
- `to-spec` and `to-tickets` may draft artifacts quickly, but their output must still satisfy this repo's layer and readiness rules.
- `handoff` is preferred whenever a session becomes recap-heavy or exceeds its `Session Budget`.
- Companion-skill enforcement should start as recommended guidance and move into validators only after local measurement proves the rule is worth the friction.

## Source Hierarchy

1. `docs/design` — approved requirements, architecture, contracts, and domain behavior
2. `docs/implementation` — execution planning: project, phases, tasks, status
3. `docs/changes/wayfinding` — decision maps for large unresolved efforts; planning aid only
4. `docs/changes/proposed` — concrete unresolved ideas, open questions, proposed deltas

## Layer Rules

- Large foggy efforts start in `docs/changes/wayfinding`.
- New behavior not present in design starts in `docs/changes/proposed`.
- Execution work starts in `docs/implementation` only after design truth exists.
- Status reporting is isolated to `docs/implementation/status`.
- Do not duplicate truth across layers.
- Do not define net-new behavior in `docs/implementation`.
- `docs/changes/wayfinding` and `docs/changes/proposed` are not approved truth.

## Parallel Agent Safety

Multiple agents can work concurrently when:
- Each task has a disjoint `Scope Boundary` — no two active tasks own the same files or modules.
- Shared modules are touched by at most one task at a time; other tasks that depend on them are blocked until that task is done.
- No task assumes another task's output unless listed under `Dependencies`.
- Each task declares a `Session Budget` with stop and handoff conditions.

## Facts vs Decisions

- Facts are discovered by reading code, docs, tests, logs, or primary sources.
- Decisions are resolved by humans, approved docs, or explicit review outcomes.
- Do not ask humans for facts the repo can answer.
- Do not let agents invent decisions because a fact was missing.
- Capture hard-to-reverse decisions in durable artifacts, not only in chat.

## Session Economics

- One execution session should target one task.
- Prefer references to existing artifacts over restating settled detail in prompts.
- When a session becomes mostly recap, create a handoff and resume in a fresh session.
- Use AFK or headless runs only for bounded tasks with explicit stop conditions.
- Design docs and task docs must be short enough to reread cheaply.

## Feature Inventory

- `docs/implementation/feature-inventory/` is the cross-phase register of every platform capability, its contribution to target capability, and its delivery status.
- One directory per feature (e.g. `auth/`, `booking/`, `selling/`); one small file per subfeature; a `README.md` index at the root and per feature.
- Create it from `templates/feature-inventory/`. Policy: `spec/feature-inventory-spec.md`.
- It is an execution-planning rollup: it traces every subfeature file to `docs/design/`, and it does not replace dated logs in `docs/implementation/status/`.
- The feature / subfeature split mirrors the decomposition of the idea in `docs/design/`; the backlog, phases, and tasks reference subfeature files by path and never redefine their behavior.
- Populate it as planning proceeds: adopting a proposal creates `Pending` subfeature files; backlog and phase breakdown fills in evidence links; execution and review move statuses.
- Update a subfeature `Status` whenever a linked backlog entry, phase, or task changes status; add a feature directory or subfeature file whenever planning produces a behavior it does not yet show.

## Content Style

Apply to every doc in every layer:

- **Brevity**: one idea per bullet, one purpose per section. Remove words that add length without adding precision.
- **Structure**: use headings, bullets, tables, and checklists. No narrative paragraphs.
- **Directness**: state what must happen. Not what might, could, or should happen.
- **Agent-executable**: every sentence is a directive, constraint, or fact. Avoid explanation of obvious behavior.
- **No filler**: remove "in order to", "it is important to", "please note", "as mentioned".
- **Concrete**: reference specific files, commands, endpoints, states, and behaviors — not abstract intent.

## Required Behaviors

- Use wayfinding before spec-writing when the route is still foggy.
- Do not invent behavior in implementation docs.
- Track progress through tasks and phases, not ad hoc notes.
- Capture unresolved or ambiguous behavior only in proposals.
- Do not start execution without a task that passes the readiness standard and declares a session budget.
- Do not mark a task done without verification evidence.
