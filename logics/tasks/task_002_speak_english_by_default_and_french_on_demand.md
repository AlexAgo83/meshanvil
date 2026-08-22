## task_002_speak_english_by_default_and_french_on_demand - Speak English by default and French on demand
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: codex
> Indicators reviewed: 2026-08-22 01:11:06

# AI Context
- Summary: Route CLI and viewer copy through the English and French catalogues, validate their parity, and preserve machine-readable report identifiers.
- Keywords: speak, english, default, french, demand
- Use when: Adding operator-facing CLI or viewer text, changing locale selection, or maintaining catalogue validation.
- Skip when: Changing warning codes, report field names, or operation names; those are stable identifiers.

# Definition of Done (DoD)
- [x] The backlog scope is implemented.
- [x] Acceptance criteria are covered.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# Backlog
- `item_010_speak_english_by_default_and_french_on_demand`

# Acceptance criteria
- AC1: No operator-facing string is written inline; every one resolves through the catalogue.
- AC2: English is the default and the fallback: a key missing from French renders in English rather than as a key.
- AC3: The parity check fails on a key present in one catalogue only, on a placeholder mismatch, and on a key nothing reads.
- AC4: MESHANVIL_LANG selects the language, the system locale is used when it is unset, and English is used when neither resolves.
- AC5: Warning codes, report field names and operation names are identical in both languages.

# AC Traceability
- request-AC17 -> This task. Proof: f84e209 through dab2494; `make check`, `make fixture`, and `logics-manager i18n validate` passed.

# Plan
- [x] Use `python3 -m logics_manager flow progress task task_002_speak_english_by_default_and_french_on_demand.md --progress <n>%` during multi-wave work.
- [x] Run `python3 -m logics_manager flow finish task task_002_speak_english_by_default_and_french_on_demand.md` after implementation.

# Validation
- `make check && make fixture && logics-manager lint --require-status && logics-manager audit --group-by-doc && logics-manager i18n validate` passed on 2026-08-22.
- Finish workflow executed on 2026-08-22.
- Linked backlog/request close verification passed.

# Report
- Not started.
- Finished on 2026-08-22.
- Linked backlog item(s): `item_010_speak_english_by_default_and_french_on_demand`
- Related request(s): `req_000_make_every_3d_operation_reviewable_without_reopening_blender`

# Links
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

# Evidence
- AC1 | date: 2026-08-22 | command: `logics-manager i18n validate` | result: passed | English/French catalogue parity and placeholders passed validation.
