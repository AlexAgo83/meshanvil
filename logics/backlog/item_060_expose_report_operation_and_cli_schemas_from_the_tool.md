## item_060_expose_report_operation_and_cli_schemas_from_the_tool - Expose report operation and CLI schemas from the tool
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
- Summary: Add schema subcommands so agents can learn report, operation manifest and CLI JSON shapes from meshanvil itself.
- Keywords: schema command, report schema, operation schema, CLI envelope
- Use when: implementing the `meshanvil schema ... --json` surface.
- Skip when: validating historical reports or changing report semantics.

# Problem
- An agent has to infer the report, operation and CLI JSON shapes from source code and examples, which makes integration brittle and version-dependent.

# Scope
- In:
  - `meshanvil schema report --json` for the report object shape the viewer and runner expect.
  - `meshanvil schema operation --json` for operation manifests under `tools`.
  - `meshanvil schema cli --json` for the top-level CLI JSON success and error envelopes.
  - One selfcheck and pytest wrapper proving each schema command prints parseable JSON with required fields.
- Out:
  - A full external JSON Schema package dependency.
  - Runtime validation of every historical report during normal commands.
  - Changing the report format.

# Acceptance criteria
- AC1: Each schema subcommand prints JSON to stdout and no human preamble.
- AC2: The report schema names required top-level report fields and the optional sections the viewer consumes.
- AC3: The operation schema names required manifest fields, parameter field shapes and known parameter types.
- AC4: The CLI schema describes the success envelope, error envelope and common command-specific payload fields.
- AC5: `make check` fails if any schema command stops producing parseable JSON.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: Each schema subcommand prints JSON to stdout and no human preamble.
- request-AC8 -> This backlog slice. Proof: AC2: The report schema names required top-level report fields and the optional sections the viewer consumes.

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
