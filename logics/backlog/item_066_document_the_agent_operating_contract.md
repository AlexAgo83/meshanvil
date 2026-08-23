## item_066_document_the_agent_operating_contract - Document the agent operating contract
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Low
> Theme: Agent-facing CLI contract
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 11:22:01

# AI Context
- Summary: Write the short AI operator playbook: JSON-first workflow, report-first reading, `work/in` safety and Logics evidence usage.
- Keywords: AI docs, agent playbook, JSON workflow, work in safety
- Use when: documenting how agents should operate meshanvil safely.
- Skip when: writing general contributor setup or vendor-specific prompts.

# Problem
- The project has contributor instructions, but no short operator-facing contract for AI tools that only need to use meshanvil safely.

# Scope
- In:
  - A short `docs/AI.md` or equivalent linked from the repository entry points.
  - Canonical command sequence: `status --json`, `schema ... --json`, `list --json`, `doctor --json`, `run ... --json`, `reports ... --json`.
  - Safety rules: do not write to `work/in`, do not commit `work/`, prefer report JSON over stdout, and keep client/source names out of docs.
  - Logics rule: use `--evidence TASK:AC` when implementing an active Logics task.
- Out:
  - General contributor setup documentation.
  - Prompt templates for a specific vendor.
  - Long tutorials.

# Acceptance criteria
- AC1: The doc is under version control and linked from an obvious existing entry point.
- AC2: It names the JSON commands and the report-first workflow.
- AC3: It states safety and privacy rules for `work/`, `work/in` and committed docs.
- AC4: It is short enough for an agent to load as context without replacing the full docs.

# AC Traceability
- request-AC7 -> This backlog slice. Proof: AC1: The doc is under version control and linked from an obvious existing entry point.
- request-AC8 -> This backlog slice. Proof: AC2: It names the JSON commands and the report-first workflow.

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
