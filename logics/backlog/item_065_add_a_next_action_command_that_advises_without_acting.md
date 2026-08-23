## item_065_add_a_next_action_command_that_advises_without_acting - Add a next action command that advises without acting
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Agent-facing CLI contract
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 11:22:01

# AI Context
- Summary: Add a pure advisory `next --json` command that suggests safe commands from current project state without mutating anything.
- Keywords: next json, advice, safe action, no mutation
- Use when: implementing agent guidance or shared status-derived advice.
- Skip when: adding automation that executes suggested commands.

# Problem
- Agents need a safe way to ask what to do next, but the product should not hide state changes behind advice.

# Scope
- In:
  - `meshanvil next --json` returning ordered action objects with reason codes, command strings and risk notes where needed.
  - Advice for no project marker, failed setup, no reports, reports present, no operations found, and viewer useful.
  - Shared status-gathering logic with `status --json` where that removes duplication.
- Out:
  - Running the commands it suggests.
  - Picking operation parameters for a source file.
  - Writing Logics evidence.

# Acceptance criteria
- AC1: `next --json` never modifies `work/`, starts a server, launches Blender, or writes reports.
- AC2: Each action includes `reason`, `command` and `description` fields.
- AC3: Advice is deterministic for the same project state.
- AC4: Selfcheck covers at least no project marker, unhealthy setup, empty reports and existing reports.

# AC Traceability
- request-AC6 -> This backlog slice. Proof: AC1: `next --json` never modifies `work/`, starts a server, launches Blender, or writes reports.
- request-AC8 -> This backlog slice. Proof: AC2: Each action includes `reason`, `command` and `description` fields.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_014_an_agent_ready_command_surface_for_meshanvil`
- Architecture decision(s): (none yet)
- Request: `req_014_make_the_cli_a_dependable_surface_for_ai_operators`
- Primary task(s): `task_027_deliver_the_agent_ready_cli_contract`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.
