## item_008_read_the_method_from_the_reports_runbook_reverse_index - Read the method from the reports: runbook reverse index
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 99%
> Complexity: High
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 01:11:06

# AI Context
- Summary: The wiki links a report already carries, read in both directions: a report leads to its runbook, and a runbook lists the operations that applied it.
- Keywords: reverse index, wiki links, document chips, runbook coverage, Logics conventions
- Use when: Navigating between an operation and the method it applied.
- Skip when: Editing runbooks, or the report format itself.

# Problem
- A report names the runbook it applied, but nothing reads that relation the other way, so no one can see which operations applied a given procedure.
- A runbook that nothing applies is invisible: it may be dormant, or the procedure may have been bypassed, and both matter.
- Document references are shown as raw slugs, which are unreadable in a dense interface.

# Scope
- In:
  - A reverse index built from the links already present in the reports: for each runbook, the operations that cite it.
  - Document chips following the Logics viewer convention exactly -- R request, I backlog, T task, P product, A architecture, S spec, M roadmap, N runbook -- with the same hues.
  - Chips that navigate: from a runbook to an operation, and from an operation back to its runbook.
  - Titles and statuses read from the corpus through the bridge of `item_013_bridge_reports_into_the_logics_corpus`, never from a table kept here.
  - Runbooks with no operation shown as such, rather than omitted.
- Out:
  - Rendering the runbook documents themselves. That is the Logics viewer's job, and adr_002 keeps that boundary.
  - Writing or editing links. The reports are the source; the index is derived.
  - Any index stored on disk: it is computed from the reports at read time.

# Acceptance criteria
- AC1: For each runbook, the operations that cite it are listed, derived from the reports and from nothing else.
- AC2: A runbook cited by no operation is shown as not yet applied.
- AC3: Chips use the Logics prefixes and hues, with the runbook prefix N as that convention requires.
- AC4: A chip navigates in both directions between an operation and a document.
- AC5: The file keeps the full slug; the chip is a rendering, never a storage format.

# AC Traceability
- request-AC15 -> This backlog slice. Proof: AC1: For each runbook, the operations that cite it are listed, derived from the reports and from nothing else.
- request-AC5 -> This backlog slice, partially. Proof: AC4: A chip navigates in both directions between an operation and a document.

# Decision framing
- Product framing: Not needed
- Product signals: (none detected)
- Product follow-up: No product brief follow-up is expected based on current signals.
- Architecture framing: `adr_002_depend_on_logics_manager_and_reuse_its_structure`
- Architecture signals: (none detected)
- Architecture follow-up: No architecture decision follow-up is expected based on current signals.

# Links
- Product brief(s): (none yet)
- Architecture decision(s): `adr_002_depend_on_logics_manager_and_reuse_its_structure`
- Request: `logics/request/req_000_make_every_3d_operation_reviewable_without_reopening_blender.md`
- Primary task(s): (none yet)

# Priority
- Priority: Medium
- Rationale: Default until groomed.

# Notes
- Hybrid rationale: Derived from request `req_000_make_every_3d_operation_reviewable_without_reopening_blender` and kept bounded to one coherent delivery slice.
- Source file: `logics/request/req_000_make_every_3d_operation_reviewable_without_reopening_blender.md`.
- Generated locally by logics-manager.

# Tasks
- `task_006_read_the_method_from_the_reports_runbook_reverse_index`
