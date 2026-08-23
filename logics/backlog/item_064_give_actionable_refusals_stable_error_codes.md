## item_064_give_actionable_refusals_stable_error_codes - Give actionable refusals stable error codes
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
- Summary: Add stable refusal codes for the failures agents can recover from without parsing translated prose.
- Keywords: refusal code, unknown operation, missing source, target busy, invalid parameter
- Use when: mapping runner and CLI refusals to machine-readable error codes.
- Skip when: changing report warning codes or adding automatic recovery.

# Problem
- An agent can recover from many refusals, but today it must parse translated text to distinguish missing files, unknown operations, invalid parameters and busy targets.

# Scope
- In:
  - Stable error codes for unknown operation, missing source file, engine missing, target busy, invalid parameter, malformed `--set`, unreadable input format and unavailable work directory.
  - A refusal representation that carries code plus human message without losing the current exception flow.
  - Mapping existing exception sources to codes at the boundary where the CLI prints JSON.
- Out:
  - Translating codes.
  - Changing report warning codes.
  - Recovering automatically from refusals.

# Acceptance criteria
- AC1: Each named refusal has a stable code in JSON mode.
- AC2: The human message remains present for logs and operators.
- AC3: Codes are documented by `schema cli --json`.
- AC4: Selfcheck covers at least one recovery path per named code without starting Blender.

# AC Traceability
- request-AC5 -> This backlog slice. Proof: AC1: Each named refusal has a stable code in JSON mode.
- request-AC8 -> This backlog slice. Proof: AC2: The human message remains present for logs and operators.

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
