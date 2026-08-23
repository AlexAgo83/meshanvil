## item_063_standardize_json_success_and_error_envelopes - Standardize JSON success and error envelopes
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 95%
> Confidence: 90%
> Progress: 0%
> Complexity: Medium
> Theme: Agent-facing CLI contract
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 11:22:01

# AI Context
- Summary: Put every JSON-mode command on one success/error envelope while preserving human stderr outside JSON mode.
- Keywords: JSON envelope, ok false, exit code, error object, run report path, stdout discipline
- Use when: refactoring CLI JSON output helpers.
- Skip when: changing process exit codes or localized human messages.

# Problem
- The first `--json` pass made stdout parseable for the common path, but error payloads are not yet consistent across commands and some failures expose only prose.
- `run --json` captures the runner's stdout into a `report` string. The value happens to be the report path today, but the field name says content and the shape says prose: an agent cannot tell which it is holding.

# Scope
- In:
  - One helper for JSON success and error output used by every command that accepts `--json`.
  - Top-level `ok` on success and `ok`, `exit_code`, `error.code`, `error.message` on failure.
  - Preserving existing human stderr for non-JSON mode.
  - Replacing `run --json`'s captured-stdout `report` string with `report_path`, `id` and the report `status` read back from the report file.
  - In `--json` mode, stdout carries the envelope and nothing else; diagnostics go to stderr.
- Out:
  - Changing process exit codes.
  - Changing localized human messages.
  - Adding JSON mode to every command in this slice.

# Acceptance criteria
- AC1: All current `--json` commands use the same top-level envelope.
- AC2: JSON-mode failures never print human-only text to stdout.
- AC3: Non-JSON failures keep their current human output.
- AC4: `run --json` exposes `report_path`, `id` and the report `status`; it no longer returns captured stdout as a `report` string.
- AC5: In `--json` mode, stdout parses as exactly one JSON object for every command and every outcome, including `EXIT_NO_REPORT`.
- AC6: Selfcheck proves success and failure envelope shape for list, doctor, prune and run.

# AC Traceability
- request-AC4 -> This backlog slice. Proof: AC1: All current `--json` commands use the same top-level envelope.
- request-AC6 -> This backlog slice. Proof: AC4: `run --json` exposes `report_path`, `id` and the report `status`; it no longer returns captured stdout as a `report` string.
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
