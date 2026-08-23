## item_060_expose_report_operation_and_cli_schemas_from_the_tool - Expose report operation and CLI schemas from the tool
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 95%
> Confidence: 90%
> Progress: 100%
> Complexity: Medium
> Theme: Agent-facing CLI contract
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 12:45:05

# AI Context
- Summary: Add one `schema --json` command so agents can learn report, operation manifest and CLI JSON shapes from meshanvil itself.
- Keywords: schema command, report schema, operation schema, CLI envelope
- Use when: implementing the `meshanvil schema --json` surface.
- Skip when: validating historical reports or changing report semantics.

# Problem
- An agent has to infer the report, operation and CLI JSON shapes from source code and examples, which makes integration brittle and version-dependent.

# Scope
- In:
  - One `meshanvil schema --json` command printing `{"report": ..., "operation": ..., "cli": ...}`.
  - `report`: the report object shape the viewer and runner expect.
  - `operation`: the operation manifest shape under `tools`, including parameter field shapes.
  - `cli`: the top-level JSON success and error envelopes and the error-code list.
  - One selfcheck and pytest wrapper proving the command prints parseable JSON with all three keys.
- Out:
  - A full external JSON Schema package dependency.
  - Three separate subcommands: the payload is small and an agent asks once.
  - Runtime validation of every historical report during normal commands.
  - Changing the report format.

# Acceptance criteria
- AC1: `schema --json` prints one JSON object to stdout with the `report`, `operation` and `cli` keys and no human preamble.
- AC2: The `report` section names required top-level report fields and the optional sections the viewer consumes.
- AC3: The `operation` section names required manifest fields, parameter field shapes and known parameter types.
- AC4: The `cli` section describes the success envelope, error envelope, the stable error codes and the exit codes.
- AC5: `make check` fails if `schema --json` stops producing parseable JSON or drops a key.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: `schema --json` prints one JSON object to stdout with the `report`, `operation` and `cli` keys and no human preamble.
- request-AC8 -> This backlog slice. Proof: AC2: The `report` section names required top-level report fields and the optional sections the viewer consumes.

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
