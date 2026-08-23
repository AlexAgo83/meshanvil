## item_063_standardize_json_success_and_error_envelopes - Standardize JSON success and error envelopes
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
- Summary: Put every JSON-mode command on one success/error envelope while preserving human stderr outside JSON mode.
- Keywords: JSON envelope, ok false, exit code, error object
- Use when: refactoring CLI JSON output helpers.
- Skip when: changing process exit codes or localized human messages.

# Problem
- The first `--json` pass made stdout parseable for the common path, but error payloads are not yet consistent across commands and some failures expose only prose.

# Scope
- In:
  - One helper for JSON success and error output used by every command that accepts `--json`.
  - Top-level `ok` on success and `ok`, `exit_code`, `error.code`, `error.message` on failure.
  - Preserving existing human stderr for non-JSON mode.
- Out:
  - Changing process exit codes.
  - Changing localized human messages.
  - Adding JSON mode to every command in this slice.

# Acceptance criteria
- AC1: All current `--json` commands use the same top-level envelope.
- AC2: JSON-mode failures never print human-only text to stdout.
- AC3: Non-JSON failures keep their current human output.
- AC4: Selfcheck proves success and failure envelope shape for list, doctor, prune and run.

# AC Traceability
- request-AC4 -> This backlog slice. Proof: AC1: All current `--json` commands use the same top-level envelope.
- request-AC8 -> This backlog slice. Proof: AC2: JSON-mode failures never print human-only text to stdout.

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
