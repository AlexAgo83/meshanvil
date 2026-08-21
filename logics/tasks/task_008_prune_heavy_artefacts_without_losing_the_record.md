## task_008_prune_heavy_artefacts_without_losing_the_record - Prune heavy artefacts without losing the record
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 95%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: codex
> Indicators reviewed: 2026-08-22 00:56:05

# AI Context
- Summary: Select only report-owned outputs; a dry run is read-only, while apply removes the file and changes only its lifecycle fields.
- Keywords: prune, heavy, artefacts, losing, record
- Use when: Reclaiming generated output space while retaining report provenance.
- Skip when: Handling sources under `work/in/` or regenerating an artefact.

# Definition of Done (DoD)
- [ ] The backlog scope is implemented.
- [ ] Acceptance criteria are covered.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# Backlog
- `item_004_prune_heavy_artefacts_without_losing_the_record`

# Acceptance criteria
- AC1: A dry run names every artefact it would delete, with the space it would free, and deletes nothing.
- AC2: Pruning deletes the artefact file and sets output.state to pruned with the date, leaving every other field of the report unchanged.
- AC3: A pinned artefact and an artefact cited by a runbook or Logics doc are never deleted, whatever the retention count.
- AC4: Nothing under work/in/ is ever a pruning candidate.
- AC5: The chain still renders after a prune, with the pruned node shown as pruned and its measurements still readable.

# Plan
- [ ] Use `python3 -m logics_manager flow progress task task_008_prune_heavy_artefacts_without_losing_the_record.md --progress <n>%` during multi-wave work.
- [ ] Run `python3 -m logics_manager flow finish task task_008_prune_heavy_artefacts_without_losing_the_record.md` after implementation.

# Validation
- `make check` (dry-run/apply lifecycle self-check)
- `./bin/meshanvil prune --keep 1 --dry-run`
- `node --check viewer/viewer.js`
- `git diff --check`

# Report
- Added explicit prune selection over report-owned outputs, respecting retention, pins and document citations.
- Applying a prune changes only `output.state` and `state_changed_at`; the viewer keeps and marks the node.

# Links
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)
