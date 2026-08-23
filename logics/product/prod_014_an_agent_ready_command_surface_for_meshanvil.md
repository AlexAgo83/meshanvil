## prod_014_an_agent_ready_command_surface_for_meshanvil - An agent-ready command surface for meshanvil
> Date: 2026-08-23
> Status: Settled
> Related request: `req_014_make_the_cli_a_dependable_surface_for_ai_operators`
> Related backlog: `item_060_expose_report_operation_and_cli_schemas_from_the_tool`
> Related task: `task_027_deliver_the_agent_ready_cli_contract`
> Related architecture: (none yet)
> Reminder: Update status, linked refs, scope, decisions, success signals, and open questions when you edit this doc.
> Indicators reviewed: 2026-08-23 12:45:05

# Overview
Makes meshanvil usable by AI operators through an explicit schema command, a single status view that also advises the next safe command, report access commands, stable JSON errors and a short agent playbook in `AGENTS.md`, without adding an agent runtime.

```mermaid
flowchart LR
  agent[AI operator] --> status[status with next hints]
  agent --> schema[schema]
  agent --> reports[reports]
  status --> cli[CLI JSON envelope]
  schema --> cli
  reports --> cli
  cli --> project[meshanvil project]
```

# Goals
- An AI can discover what meshanvil can do without reading Python source.
- An AI can decide the next safe command from one status response.
- An AI can list and read reports through a stable CLI contract instead of filesystem conventions.
- JSON output stays parseable and stable across locales.
- The human CLI remains friendly and unchanged unless `--json` is requested.

# Non-goals
- No autonomous planner or agent framework.
- No MCP server or background daemon.
- No change to report semantics or operation execution.
- No versioned sample data from `work/`.
- No localization of machine identifiers or error codes.

# Scope and guardrails
- In: schema, status with next-action hints, reports, stable JSON envelopes, stable refusal codes, and a short AI operator guide in `AGENTS.md`.
- Out: an agent framework, MCP server, background daemon, report semantic changes, operation execution changes, and versioned `work/` sample data.

# Key product decisions
- Keep this as CLI plus JSON. Agents get a dependable command surface, not a new runtime.
- Machine identifiers and error codes are stable and untranslated; human messages can stay localized.
- Advice is a read-only field of `status`, not its own command: it reports safe next steps and never performs them.

# Success signals
- An AI can run one status command and know the project, setup, reports and next safe actions.
- An AI can validate its expectations from schema commands instead of reading Python source.
- JSON-mode failures carry stable codes and remain parseable across locales.

# References
- Product back-reference: `item_060_expose_report_operation_and_cli_schemas_from_the_tool`
- Task back-reference: `task_027_deliver_the_agent_ready_cli_contract`
