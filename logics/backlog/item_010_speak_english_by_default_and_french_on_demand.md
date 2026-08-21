## item_010_speak_english_by_default_and_french_on_demand - Speak English by default and French on demand
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 90%
> Complexity: High
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 00:07:47

# AI Context
- Summary: Every string the tool shows comes from a catalogue, English by default and French available, with a parity check that fails when the two drift.
- Keywords: i18n, catalogues, parity check, English default, French
- Use when: Adding or changing any text the operator reads.
- Skip when: Warning codes and report field names, which are identifiers and are never translated.

# Problem
- Strings are written inline, in two languages depending on which file they are in: the pipeline prints French, the runbooks are English.
- A public repository whose interface is half French is unusable for anyone else, and a French-only tool is unusable for its own author's other projects.
- cm-sim already solved this in the same house, including the check that keeps two catalogues honest -- a key present in one and not the other, a changed placeholder, or a key nothing reads.

# Scope
- In:
  - Two catalogues, `en.json` and `fr.json`, English as the source and the fallback.
  - Every operator-facing string routed through the catalogue: CLI output, viewer interface, empty states, error messages.
  - A parity check in `make check` that fails on a key missing from one catalogue, on a placeholder that differs between them, and on a key nothing reads.
  - Language chosen by `MESHANVIL_LANG`, falling back to the system locale, then to English.
  - Warning codes, report field names and operation names left untranslated on purpose, with that rule stated where a contributor will read it.
- Out:
  - Translating the runbooks or the Logics corpus. Those are documents, not interface.
  - Right-to-left layout, pluralisation rules beyond what the catalogue format expresses, or a third language.
  - Translating anything an agent parses. A warning code is an identifier.

# Acceptance criteria
- AC1: No operator-facing string is written inline; every one resolves through the catalogue.
- AC2: English is the default and the fallback: a key missing from French renders in English rather than as a key.
- AC3: The parity check fails on a key present in one catalogue only, on a placeholder mismatch, and on a key nothing reads.
- AC4: MESHANVIL_LANG selects the language, the system locale is used when it is unset, and English is used when neither resolves.
- AC5: Warning codes, report field names and operation names are identical in both languages.

# AC Traceability
- request-AC17 -> This backlog slice. Proof: AC1: No operator-facing string is written inline; every one resolves through the catalogue.
- request-AC12 -> This backlog slice, partially. Proof: AC2: first-run text follows the same catalogue and fallback.

# Decision framing
- Product framing: Not needed
- Product signals: (none detected)
- Product follow-up: No product brief follow-up is expected based on current signals.
- Architecture framing: Not needed
- Architecture signals: (none detected)
- Architecture follow-up: No architecture decision follow-up is expected based on current signals.

# Links
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)
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
- `task_002_speak_english_by_default_and_french_on_demand`
