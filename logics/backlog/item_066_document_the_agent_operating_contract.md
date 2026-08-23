## item_066_document_the_agent_operating_contract - Document the agent operating contract
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 95%
> Confidence: 90%
> Progress: 10%
> Complexity: Low
> Theme: Agent-facing CLI contract
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 12:40:44

# AI Context
- Summary: Turn `AGENTS.md` into the AI operator playbook: JSON-first workflow, report-first reading, exit codes, `work/in` safety and Logics evidence usage.
- Keywords: AI docs, agent playbook, JSON workflow, work in safety
- Use when: documenting how agents should operate meshanvil safely.
- Skip when: writing general contributor setup or vendor-specific prompts.

# Problem
- The project has contributor instructions, but no short operator-facing contract for AI tools that only need to use meshanvil safely.
- `AGENTS.md` already exists and is the file agent tools read first, but it holds a single `@LOGICS.md` pointer: an agent lands on the contributor workflow instead of the tool contract.

# Scope
- In:
  - The contract written into `AGENTS.md`, keeping the `@LOGICS.md` pointer for contributor workflow.
  - Canonical command sequence: `status --json`, `schema --json`, `list --json`, `doctor --json`, `run ... --json`, `reports ... --json`.
  - The exit-code table: 0 ok, 1 failed, 2 refused, 3 no report -- and the rule that JSON reports the code while the process still returns it.
  - Written first against the CLI as it stands today, then revised as each slice lands: a correct doc for the current surface is already most of the value.
  - Safety rules: do not write to `work/in`, do not commit `work/`, prefer report JSON over stdout, and keep client/source names out of docs.
  - Logics rule: use `--evidence TASK:AC` when implementing an active Logics task.
- Out:
  - General contributor setup documentation.
  - Prompt templates for a specific vendor.
  - Long tutorials.

# Acceptance criteria
- AC1: The contract lives in `AGENTS.md` at the repository root and still points to `LOGICS.md` for contributor workflow.
- AC2: It names the JSON commands and the report-first workflow.
- AC3: It states safety and privacy rules for `work/`, `work/in` and committed docs.
- AC4: It is short enough for an agent to load as context without replacing the full docs.
- AC5: It states the exit codes and their meaning.

# AC Traceability
- request-AC7 -> This backlog slice. Proof: AC1: The contract lives in `AGENTS.md` at the repository root and still points to `LOGICS.md` for contributor workflow.
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
- Priority: High
- Rationale: Highest value per line of work in the request: it makes the CLI usable by an agent without shipping a single new command.
