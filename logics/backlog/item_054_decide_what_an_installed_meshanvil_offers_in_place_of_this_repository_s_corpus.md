## item_054_decide_what_an_installed_meshanvil_offers_in_place_of_this_repository_s_corpus - Decide what an installed meshanvil offers in place of this repository's corpus
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Distribution and installation
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 00:48:28

# AI Context
- Summary: Settles what the runbook workspace shows when the installation is not this repository: shipped content, the project's own, or an explained empty state.
- Keywords: runbook source, installed corpus, empty state, report document links
- Use when: Deciding what documents an installed tool can show.
- Skip when: Shipping this repository's own corpus as tool content.

# Problem
- `logics_bridge` reads runbooks from the installation, which today is this repository's own corpus. Installed, there is no corpus there, and nothing has decided whether the runbook workspace should ship content, read the project's, or say it has none.

# Scope
- In:
  - A recorded decision among shipping a runbook set, reading the project's own, or offering none with an explanation.
  - The runbook workspace and the report-to-runbook links behaving per that decision rather than failing or showing an unexplained empty pane.
- Out:
  - Shipping this repository's Logics corpus as package content, which is project history rather than tool content.

# Acceptance criteria
- AC1: The decision is recorded with its alternatives.
- AC2: An installed tool's runbook workspace matches it, and an empty state explains itself.
- AC3: A report's links to documents behave the same way rather than pointing at nothing.

# AC Traceability
- request-AC7 -> This backlog slice. Proof: AC1: The decision is recorded with its alternatives.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_012_a_tool_you_install_not_a_repository_you_clone`
- Architecture decision(s): (none yet)
- Request: `req_011_make_meshanvil_an_installable_tool_instead_of_a_repository_you_clone`
- Primary task(s): `task_025_deliver_an_installable_meshanvil`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.
