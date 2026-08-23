## req_014_make_the_cli_a_dependable_surface_for_ai_operators - Make the CLI a dependable surface for AI operators
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 95%
> Confidence: 90%
> Complexity: High
> Theme: Agent-facing CLI contract
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 12:45:04

# AI Context
- Summary: Define meshanvil's AI-facing CLI contract: schema discovery, status, report access, stable JSON errors and a short agent playbook.
- Keywords: agent CLI, JSON contract, schemas, status, reports, stable errors
- Use when: making meshanvil safer or easier for AI tools to operate through the command line.
- Skip when: changing viewer presentation, geometry operations, packaging, or human-only CLI text.

# Needs
- The CLI now has `--json` on the most useful commands for automation, but an AI still has to infer too much from scattered commands and report files. A first-time agent needs one canonical way to learn the project state, the available schemas, the reports that already exist, and what to do next.
- `doctor --json`, `list --json`, `prune --json` and `run --json` do not yet share one error envelope. Refusals still expose translated human text as the only stable value in some paths, which makes an agent parse prose instead of identifiers.
- Reports are deliberately JSON files under the runtime reports directory, but there is no CLI for listing, selecting or reading them. Agents can read the filesystem, but that makes the workflow depend on filename conventions rather than a product contract.
- The report and operation formats are mostly discoverable by reading code, manifests and examples. That is workable for a human contributor and brittle for an AI operator, which should be able to ask the tool for the schema it is expected to obey.
- There is no single `status` command that answers whether the active directory is a project, whether setup passes, whether reports exist, which operations are available, and what the next safe command is.
- There is no short agent-oriented document that states the canonical commands, the `--json` preference, the report-first workflow, the `work/in` immutability rule, and how to attach Logics evidence.

# Context
- Keep this a CLI and JSON contract change. Do not introduce an agent framework, MCP server, background daemon or new runtime dependency.
- Machine identifiers are not translated. Human messages can stay localized, but JSON fields and error codes must be stable across locales.
- The existing `scripts/selfcheck.py` plus thin pytest wrappers are the right test shape for this project. Each new machine contract needs one small check that fails if stdout stops being parseable JSON or a stable field disappears.
- The CLI's existing exit codes are part of the contract and should not change. JSON reports the exit code; the process still returns it.
- The tool already has the ingredients for `status`: `paths.resolve`, `doctor.check`, `manifests.discover`, and the reports under the runtime reports directory. The request is to expose them consistently, not to build a planner.
- Generated or runtime data under `work/` is not versioned. Docs and schemas must describe it without committing sample client paths.

# Acceptance criteria
- AC1: `meshanvil schema --json` prints one object keyed `report`, `operation` and `cli`, describing the report shape, the operation manifest shape and the JSON envelopes well enough for an AI to validate them without reading Python source. One command, not three subcommands.
- AC2: `meshanvil status --json` prints one JSON object containing project identity, setup state, operation summary, report summary, viewer hint, and ordered next-action hints (reason code + command, advice only); stdout contains no human preamble.
- AC3: `meshanvil reports --json`, `meshanvil reports --latest --json`, and `meshanvil reports <id> --json` let an agent list reports, find the latest report, and read one report without walking the runtime reports directory itself.
- AC4: Every command that accepts `--json` returns the same top-level success and error envelope: success includes `ok: true`; failures include `ok: false`, `exit_code`, and a stable `error.code` plus a human `error.message`.
- AC5: Refusals that an agent can act on have stable error codes, at least for unknown operation, missing source file, engine missing, target busy, invalid parameter, malformed `--set`, unreadable input format, and unavailable work directory.
- AC6: `run --json` returns the report as machine data, not a stdout blob: at least `report_path`, `id` and the report `status`. Every `--json` command writes the envelope and nothing else to stdout; human and diagnostic text goes to stderr.
- AC7: `AGENTS.md` carries the agent operating contract (today it is a one-line pointer to `LOGICS.md`, which is the contributor workflow, not the tool contract). It states the exit-code table and the canonical automation workflow: prefer `--json`, never write to `work/in`, discover before run, read reports rather than stdout, use `--evidence TASK:AC` when Logics is active, and keep client/source names out of committed docs.
- AC8: Each new command and envelope rule has a selfcheck plus a thin pytest wrapper, and `make check`, `logics-manager lint --require-status`, and `logics-manager audit --group-by-doc` pass.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_014_an_agent_ready_command_surface_for_meshanvil`
- Architecture decision(s): (none yet)

# References
- meshanvil/cli.py
- meshanvil/runner.py
- meshanvil/doctor.py
- meshanvil/manifests.py
- meshanvil/prune.py
- meshanvil/paths.py
- meshanvil/viewer_payload.py
- meshanvil/logics_bridge.py
- meshanvil/i18n.py
- scripts/selfcheck.py
- tests/test_cli.py
- locales/en.json
- locales/fr.json
- tools

# Backlog
- `item_060_expose_report_operation_and_cli_schemas_from_the_tool`
- `item_061_add_one_status_json_command_for_agent_preflight`
- `item_062_let_agents_list_and_read_reports_through_the_cli`
- `item_063_standardize_json_success_and_error_envelopes`
- `item_064_give_actionable_refusals_stable_error_codes`
- `item_066_document_the_agent_operating_contract`
