## item_004_prune_heavy_artefacts_without_losing_the_record - Prune heavy artefacts without losing the record
> From version: 1.0.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Low
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# AI Context
- Summary: A pruning policy that deletes heavy artefacts by rule -- keep the last N, keep anything pinned or cited by a runbook -- and records the deletion in the report it describes, so the timeline keeps no holes.
- Keywords: pruning policy, artefact lifecycle, pinned artefact, disk footprint, immutable report
- Use when: Deciding what happens to generated blends, STLs and renders over time.
- Skip when: Designing the report itself (item_001) or its display (item_003).

# Problem
- work/ fills with blends of 200 MB and STLs of 68 MB, while the reports that describe them weigh a few kilobytes. Without a policy the only options are keeping everything or deleting by hand.
- Deleting by hand loses the record along with the file: nothing then says an operation ever ran, and the chain gains a hole no one can explain later.
- A failed attempt looks like the obvious thing to delete and is the opposite: run_007's three failed approaches are the more valuable half of that runbook.

# Scope
- In:
  - A pruning rule expressed in one place: keep the last N artefacts of a chain, keep anything pinned, keep anything a runbook or a Logics doc cites.
  - Pruning sets output.state to pruned and stamps the date in the report the artefact belonged to, leaving every other field untouched.
  - A dry-run mode naming what would be deleted and how much it would free, refusing to guess.
  - The viewer showing a pruned node as pruned rather than as missing or broken.
- Out:
  - Deleting or rewriting a report. Reports are immutable except for their artefact state.
  - Pruning anything under work/in/. Sources are never touched by any operation.
  - Re-running an operation to regenerate a pruned artefact, which is the runner's job and not this slice's.
  - Any automatic scheduling. Pruning is a command the operator runs.

# Acceptance criteria
- AC1: A dry run names every artefact it would delete, with the space it would free, and deletes nothing.
- AC2: Pruning deletes the artefact file and sets output.state to pruned with the date, leaving every other field of the report unchanged.
- AC3: A pinned artefact and an artefact cited by a runbook or Logics doc are never deleted, whatever the retention count.
- AC4: Nothing under work/in/ is ever a pruning candidate.
- AC5: The chain still renders after a prune, with the pruned node shown as pruned and its measurements still readable.

# AC Traceability
- request-AC10 -> This backlog slice. Proof: AC2: Pruning deletes the artefact file and sets output.state to pruned with the date, leaving every other field of the report unchanged.
- request-AC9 -> This backlog slice, partially. Proof: AC5: The chain still renders after a prune, with the pruned node shown as pruned and its measurements still readable.

# Decision framing
- Product framing: Not needed
- Product signals: (none detected)
- Product follow-up: No product brief follow-up is expected based on current signals.
- Architecture framing: `adr_001_operation_report_format`
- Architecture signals: (none detected)
- Architecture follow-up: No architecture decision follow-up is expected based on current signals.

# Links
- Product brief(s): (none yet)
- Architecture decision(s): `adr_001_operation_report_format`
- Request: `logics/request/req_000_make_every_3d_operation_reviewable_without_reopening_blender.md`
- Primary task(s): (none yet)

# Priority
- Priority: Medium
- Rationale: Default until groomed.

# Notes
- Hybrid rationale: Derived from request `req_000_make_every_3d_operation_reviewable_without_reopening_blender` and kept bounded to one coherent delivery slice.
- Source file: `logics/request/req_000_make_every_3d_operation_reviewable_without_reopening_blender.md`.
- Generated locally by logics-manager.
