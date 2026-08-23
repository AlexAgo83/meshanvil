## item_061_add_one_status_json_command_for_agent_preflight - Add one status JSON command for agent preflight
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Agent-facing CLI contract
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 11:21:52

# AI Context
- Summary: Add one JSON preflight command that combines project, setup, operations, report summary, viewer hint and next hints.
- Keywords: status json, preflight, project state, report summary
- Use when: implementing `meshanvil status --json` or shared status collection.
- Skip when: adding operation execution, report mutation or viewer startup behavior.

# Problem
- A first-time agent must call several commands and inspect files to know whether it is in a project, whether setup passes, what operations exist, and whether reports already exist.

# Scope
- In:
  - `meshanvil status --json` combining project resolution, `doctor.check`, `manifests.discover`, report counts and latest report metadata.
  - A viewer hint that says whether `meshanvil view` is a useful next action without starting it.
  - A small list of next-action hints, each with a stable reason code and a command string.
- Out:
  - Starting the viewer or running setup checks beyond what `doctor.check` already does.
  - A planner that chooses operation parameters.
  - Human table output; this command can be JSON-only initially.

# Acceptance criteria
- AC1: `status --json` prints one parseable object with `ok`, `project`, `doctor`, `operations`, `reports`, `viewer` and `next` keys.
- AC2: The command exits with the same refused status as `doctor` when required setup is missing, while still printing the JSON object.
- AC3: Report summary includes count and latest report id/path when present, but does not read every large artefact.
- AC4: Next-action hints are ordered and include stable reason codes.
- AC5: Selfcheck covers both a healthy and an unhealthy project.

# AC Traceability
- request-AC2 -> This backlog slice. Proof: AC1: `status --json` prints one parseable object with `ok`, `project`, `doctor`, `operations`, `reports`, `viewer` and `next` keys.
- request-AC8 -> This backlog slice. Proof: AC2: The command exits with the same refused status as `doctor` when required setup is missing, while still printing the JSON object.

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
