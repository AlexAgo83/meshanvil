## item_074_let_a_human_say_what_the_numbers_do_not_without_touching_the_reports - Let a human say what the numbers do not, without touching the reports
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 10%
> Complexity: Medium
> Theme: Annotations over machine records
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-25 00:23:17

# AI Context
- Summary: A report says what an operation did and nothing about why it mattered, which parameter was a guess, or what the next attempt should change. The storage decision is the substance: annotations stay outside the reports, because the reports' value is that every number in them came out of an engine. An agent returning to a chain is a first-class reader, so the file has to be readable with cat.
- Keywords: report note, chain name, annotations outside reports, flat JSON sidecar, sha256 keying, read-only file protocol page
- Use when: Adding operator-written content to the viewer, or deciding where anything a human writes is stored.
- Skip when: The work would put prose inside a report -- that is the one thing this item exists to avoid.

# Problem
- A report says what an operation did and nothing about why it was worth doing, which parameter was a guess, or what the next attempt should change.
- An operator returning to a chain, and an agent picking one up later, both read the same numbers with none of the reasoning.
- A chain is named after its source file, so two chains from similar files are told apart by reading paths and neither can be given the name the work actually has.
- Writing any of this into the reports would put human prose inside the record whose whole value is that every number in it came out of an engine.

# Scope
- In:
  - A note per report and a name per chain, written and edited from the page.
  - One flat JSON file outside the reports, readable with `cat` because an agent returning to a chain is a first-class reader of it.
  - Notes keyed by report identity; chain names keyed by the sha256 of the source file, so a name survives the file being moved and does not follow a regenerated file.
  - A visual treatment that cannot be mistaken for something the tool measured.
  - Refusing writes on a file:// page, which has no server to write through.
- One guarded POST route on the served server, under the decision recorded in `adr_009`: the same per-launch token as the run and file routes, the same origin and host refusals, serialised writes, and no path ever taken from the request.
- Writing the file atomically -- temporary file in the same directory, then rename -- so a crash or a second writer leaves a stale file and never a truncated one.
- Deciding and implementing what happens to a note whose report `prune` has deleted, since `prune` knows nothing about annotations today.
  - Checks: the key rules in viewer/src without a DOM, the write path in the Python checks, and the round trip in the browser smoke.
- Out:
  - Threads, replies, authorship or timestamps beyond what a single note needs.
- Reconciling two pages editing the same project at once: last writer wins, as `adr_009` records.
  - Notes on anything other than a report or a chain.
  - Rendering Markdown inside a note.
  - Versioning the annotation file, or reconciling concurrent edits from two pages.

# Acceptance criteria
- AC1: A note can be written, edited and cleared on any report from the page, and survives a live refresh, a reload and a server restart.
- AC2: A chain can be given a name that is shown wherever the chain is named, and the source file name remains visible.
- AC3: Annotations live in one flat JSON file outside work/ops, and no report file is modified by writing one.
- AC4: A chain name is keyed by the source file's sha256: moving the file keeps the name, regenerating the file does not inherit it.
- AC5: A file:// page shows existing annotations and refuses to write, saying why.
- AC6: A Python check fails if writing an annotation modifies any file under work/ops.
- AC7: The write route requires the per-launch token and is refused without it, on a foreign Host and on a foreign Origin, like the two POST routes that already exist.
- AC8: A write interrupted partway leaves the previous annotation file intact and readable, never a truncated one.
- AC9: After `prune` removes a report, its note is handled by a stated rule rather than left to rot silently, and a check covers whichever rule is chosen.

# AC Traceability
- request-AC7 -> This backlog slice. Proof: AC1: A note can be written, edited and cleared on any report from the page, and survives a live refresh, a reload and a server restart.
- request-AC8 -> This backlog slice. Proof: AC2: A chain can be given a name that is shown wherever the chain is named, and the source file name remains visible.
- request-AC9 -> This backlog slice. Proof: AC3: Annotations live in one flat JSON file outside work/ops, and no report file is modified by writing one.
- request-AC10 -> This backlog slice. Proof: AC7: The write route requires the per-launch token and is refused without it, on a foreign Host and on a foreign Origin, like the two POST routes that already exist. The decision itself is recorded in `adr_009_let_the_served_viewer_write_annotations_and_nothing_else`.

# Decision framing
- Product framing: Not needed
- Architecture framing: `adr_009_let_the_served_viewer_write_annotations_and_nothing_else`

# Links
- Product brief(s): `prod_015_a_viewer_that_keeps_up_with_the_work`
- Architecture decision(s): (none yet)
- Request: `req_016_make_the_viewer_s_outliner_refresh_and_annotations_hold_up_in_daily_use`
- Primary task(s): `task_029_deliver_the_viewer_s_fold_refresh_payload_and_annotation_work`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.
