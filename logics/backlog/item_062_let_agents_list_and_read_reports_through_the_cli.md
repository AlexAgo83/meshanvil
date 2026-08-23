## item_062_let_agents_list_and_read_reports_through_the_cli - Let agents list and read reports through the CLI
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Agent-facing CLI contract
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 12:45:05

# AI Context
- Summary: Add report listing, latest-report and report-by-id CLI access so agents do not walk `work/ops` directly.
- Keywords: reports json, latest report, report id, work ops
- Use when: implementing `meshanvil reports ... --json`.
- Skip when: changing report filenames, report contents or artefact opening.

# Problem
- Reports are the product's main record, but agents must currently walk `work/ops` and understand filename conventions to find or read them.

# Scope
- In:
  - `meshanvil reports --json` returning sorted report summaries.
  - `meshanvil reports --latest --json` returning the latest report object or a stable not-found error.
  - `meshanvil reports <id> --json` resolving ids like `003` and `003a` to the matching report file and returning its parsed JSON plus path metadata.
- Out:
  - Searching inside reports by arbitrary query.
  - Opening artefacts or renders.
  - Changing report filenames.

# Acceptance criteria
- AC1: Report listing includes id, operation, status, path, input path when present, output path/state when present, and created/readable timestamp if available.
- AC2: Latest report resolution is deterministic and matches current filename ordering rules.
- AC3: Reading a report by id returns exactly one report or a stable ambiguous/not-found error.
- AC4: Malformed report files are reported in the listing with a stable warning field rather than crashing the command.
- AC5: Selfcheck covers empty, malformed, single-report and ambiguous-id cases.

# AC Traceability
- request-AC3 -> This backlog slice. Proof: AC1: Report listing includes id, operation, status, path, input path when present, output path/state when present, and created/readable timestamp if available.
- request-AC8 -> This backlog slice. Proof: AC2: Latest report resolution is deterministic and matches current filename ordering rules.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_014_an_agent_ready_command_surface_for_meshanvil`
- Architecture decision(s): (none yet)
- Request: `req_014_make_the_cli_a_dependable_surface_for_ai_operators`
- Primary task(s): `task_027_deliver_the_agent_ready_cli_contract`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_027_deliver_the_agent_ready_cli_contract`

# Notes
- Task `task_027_deliver_the_agent_ready_cli_contract` was finished via `logics-manager flow finish task` on 2026-08-23.
