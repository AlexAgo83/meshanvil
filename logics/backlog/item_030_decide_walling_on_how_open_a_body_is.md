## item_030_decide_walling_on_how_open_a_body_is - Decide walling on how open a body is
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 85%
> Complexity: Low
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 14:02:34

# AI Context
- Summary: Walling skips a body only at exactly zero open edges. A sculpt with 4 open edges out of 14 803 faces was walled, doubling its vertices and hollowing a solid body, and the report said `walled 1` without saying that was wrong.
- Keywords: skip_closed, openness ratio, hollowed body, walling decision, per-object record
- Use when: changing how walling decides what to thicken, or what it records per object.
- Skip when: the change is about wall thickness or the spike guard rather than the decision to wall at all.
# Problem
- Walling skips a body only when it has exactly zero open edges.
- A sculpt with 4 open edges out of 14 803 faces was walled, doubling its vertices and hollowing a solid body.
- The report recorded `walled 1, already_closed 0`, which is true and tells the reader nothing about the decision being wrong.

# Scope
- In:
  - Judge a body by how open it is against a stated tolerance rather than by a zero test.
  - For a body closed within tolerance, repair the seam or leave it alone rather than thickening it.
  - Record the openness measured and the decision taken for every object.
- Out:
  - Repairing arbitrary non-manifold geometry.
  - Guessing the operator's intent when a body is genuinely half open.

# Acceptance criteria
- AC1: The walling decision uses a stated openness tolerance, not a zero test.
- AC2: A body closed within tolerance is not thickened, and the report says which rule applied to it.
- AC3: The sculpt case is asserted: a body with a handful of open edges out of thousands of faces keeps its vertex count.
- AC4: A genuinely open panel is still walled, so the vehicle chain is unchanged.

# AC Traceability
- request-AC3 -> This backlog slice. Proof: AC1: The walling decision uses a stated openness tolerance, not a zero test.
- request-AC4 -> This backlog slice. Proof: AC2: A body closed within tolerance is not thickened, and the report says which rule applied to it.
- request-AC6 -> This backlog slice. Proof: AC3: The sculpt case is asserted: a body with a handful of open edges out of thousands of faces keeps its vertex count.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_006_guards_that_measure_what_they_claim`
- Architecture decision(s): (none yet)
- Request: `req_005_fix_the_guards_that_pass_while_the_geometry_is_wrong`
- Primary task(s): `task_019_fix_the_guards_that_pass_while_the_geometry_is_wrong`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.
