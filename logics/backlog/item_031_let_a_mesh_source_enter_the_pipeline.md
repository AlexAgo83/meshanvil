## item_031_let_a_mesh_source_enter_the_pipeline - Let a mesh source enter the pipeline
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 85%
> Complexity: Low
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 14:02:34

# AI Context
- Summary: The only import operation reads STEP through FreeCAD, so a subject delivered as a mesh file has to be converted by a hand-run script that leaves no report and no fingerprint. The chain then starts with no recorded input.
- Keywords: mesh import, OBJ, chain entry, source fingerprint, recorded operation
- Use when: bringing a source into the pipeline that is not already a .blend.
- Skip when: the source is already a .blend, or the question is about geometry rather than entry.
# Problem
- The only import operation reads STEP and needs FreeCAD.
- A subject delivered as a mesh file alone has to be converted with a hand-run script, which leaves no report and no fingerprint.
- That breaks the chain at its first link: the imported state has no recorded parent and no recorded input.

# Scope
- In:
  - One recorded operation that reads a common mesh interchange file and writes an artefact the chain can continue from.
  - Record the source fingerprint and the counts on both sides, as every other operation does.
  - Cover the formats there is a real source for in this project.
- Out:
  - A format matrix, a conversion service, or formats nobody here has a file for.
  - Material, texture or rig import.

# Acceptance criteria
- AC1: A mesh source outside the .blend format enters the chain through an operation that writes a report.
- AC2: The report records the source fingerprint, the counts read, and the artefact written.
- AC3: The operation refuses a file it cannot read with a stated reason rather than writing a partial artefact.

# AC Traceability
- request-AC5 -> This backlog slice. Proof: AC1: A mesh source outside the .blend format enters the chain through an operation that writes a report.
- request-AC6 -> This backlog slice. Proof: AC2: The report records the source fingerprint, the counts read, and the artefact written.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_006_guards_that_measure_what_they_claim`
- Architecture decision(s): (none yet)
- Request: `req_005_fix_the_guards_that_pass_while_the_geometry_is_wrong`
- Primary task(s): `task_019_fix_the_guards_that_pass_while_the_geometry_is_wrong`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.
