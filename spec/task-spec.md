# Task Spec

## Purpose

A task is the primary artifact an agent executes against. It must be prepared to the point where an agent can operate without improvisation — no scope inference, no behavior invention, no judgment calls about what "done" means.

## Minimum Viable Task

A task is ready for execution when all required sections are populated:

| Section | Required content |
|---|---|
| `Objective` | One sentence: what must be true when this task is done |
| `Scope Boundary` | Explicit in-scope files/modules and out-of-scope boundaries |
| `Acceptance Criteria` | Binary verifiable conditions — each must be checkable without judgment |
| `Agent Context` | Skills to load, design docs to read, constraints and do-not-touch boundaries |
| `Session Budget` | Execution mode, stop conditions, and handoff trigger |
| `Implementation Checklist` | Ordered steps the agent should follow |
| `Verification` | Exact command to run or evidence to produce |

## Agent Context Format

```
- Skills: <skill-name>, <skill-name>
- Design docs: <path>, <path>
- Constraints: <constraint>
- Do not touch: <path or module>
```

Skills tell the agent which domain knowledge to load. Design docs tell it what to read before starting. Constraints are non-negotiable rules. Do-not-touch prevents scope creep into adjacent areas.

## Session Budget Format

```
- Mode: interactive | afk
- Stop when: <explicit completion or abort conditions>
- Handoff when: <context or uncertainty trigger>
```

Use `interactive` by default. Use `afk` only when the task is bounded enough that the agent can stop safely without more human judgment.

## Acceptance Criteria Rules

Each criterion must be:

- Binary: passes or fails — no partial states.
- Judgment-free: a second agent reading it reaches the same pass/fail conclusion.
- Specific: references an HTTP method, endpoint, command, file, state, or observable output.

Bad: `The auth flow works correctly.`
Good: `POST /auth/login returns 200 with a signed JWT when credentials are valid.`

The validator checks that the section is non-empty. Criterion quality is enforced at task review, not by script.

## Vertical Slice Rule

Default to vertical slices, not horizontal layers.

- Good: one thin behavior that crosses schema, service, API, UI, and verification end to end.
- Bad: "build all database migrations" or "write all frontend screens" with no independently verifiable behavior.

Wide refactors are the exception. When a change cannot land safely as one slice, use expand → migrate → contract and state that strategy in the task.

## Parallel Agent Boundary

When multiple tasks run concurrently:

- Each task's `Scope Boundary` must be disjoint from all other `in-progress` tasks.
- Two tasks may not own the same file or module simultaneously.
- If a task needs a shared module that another task owns, list that task under `Dependencies` and keep status `pending` until it completes.
- `blocked` tasks must satisfy the readiness gate before transitioning to `in-progress`. A task blocked on unclear requirements is not ready for execution; resolve requirements before unblocking.
- If a session becomes recap-heavy or drifts beyond its budget, hand off instead of continuing in the same thread.

Scope conflict across active tasks is enforced by the `SCOPE` validator check.

## What Makes a Bad Task

- Objective is vague — agent must infer what done means.
- No acceptance criteria — agent self-declares done.
- No scope boundary — agent guesses what is in scope.
- No agent context — agent improvises which skills or docs to use.
- No session budget — agent runs until context is noisy or expensive.
- Verification is absent or a placeholder — no way to confirm correctness.
