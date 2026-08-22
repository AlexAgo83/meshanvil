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
> Indicators reviewed: 2026-08-23 01:05:30

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

# Implementation anchors
> Line numbers read at `50e5b00`; treat them as a starting point, not a contract -- the named function or literal is the anchor that survives an edit.

- The dependency is a subprocess, not an import: `logics_bridge.call()` (`meshanvil/logics_bridge.py:7`) shells out to `logics-manager` and returns `(None, "unavailable")` when it is absent -- so an installed tool without the corpus tooling already degrades rather than crashing. The question is what it should *show*, not whether it survives.
- Three consumers to keep consistent with whatever is decided: `runbooks()` (`meshanvil/logics_bridge.py:43`) fills the runbook workspace, `documents()` (`:35`) resolves the doc chips a report links to, and `runbook()` (`:76`) is the `meshanvil runbook <chain>` command (`meshanvil/cli.py:82`).
- `purpose()` (`meshanvil/logics_bridge.py:52`) reads a line out of each runbook file directly, so the runbook workspace needs the files themselves, not just metadata -- shipping "just the index" is not one of the options.
- The viewer already lists runbooks nobody has applied, deliberately (`meshanvil/viewer.py:90` says why). An empty workspace is therefore a state the design already has an opinion about.
- `adr_006_bridges_between_meshanvil_and_logics` is the decision this amends.
- Recommendation, to argue with rather than to follow: read the runbooks of the project the tool is pointed at, ship none. It is the only option consistent with what already exists -- `logics_bridge` resolves against a root rather than a bundled copy, the installation-versus-project split already says a project holds its own work, shipping this repository's runbooks is already a non-goal of the request, and the empty state has a design opinion behind it (`meshanvil/viewer.py:90` explains why a runbook nobody has applied stays listed). The ADR may still choose otherwise; this is a starting position, not the decision.

# Decision framing
- Product framing: Not needed
- Architecture framing: Needed: what an installed tool offers in place of this repository's corpus -- runbooks shipped, read from the project, or absent with an explanation. Touches `adr_006_bridges_between_meshanvil_and_logics`.

# Links
- Product brief(s): `prod_012_a_tool_you_install_not_a_repository_you_clone`
- Architecture decision(s): (none yet)
- Request: `req_011_make_meshanvil_an_installable_tool_instead_of_a_repository_you_clone`
- Primary task(s): `task_025_deliver_an_installable_meshanvil`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.
