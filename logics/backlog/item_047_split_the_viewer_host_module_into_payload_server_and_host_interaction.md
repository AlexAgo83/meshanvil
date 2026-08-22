## item_047_split_the_viewer_host_module_into_payload_server_and_host_interaction - Split the viewer host module into payload, server and host interaction
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Runtime architecture and code structure
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 00:37:30

# AI Context
- Summary: The viewer's three host jobs -- payload, HTTP serving, host interaction -- separate, behind a route convention where a new endpoint never grows the dispatcher.
- Keywords: module split, route convention, dispatcher, closed command set unchanged
- Use when: Adding a route to the viewer's server, or changing how it is organised.
- Skip when: Changing what any existing route does.

# Problem
- `meshanvil/viewer.py` computes the payload, serves HTTP and launches a browser in one 199-line module, and the data route, the event stream and `req_009`'s open/reveal route would all land in it.

# Scope
- In:
  - Separating the three jobs into their own modules behind the same public entry point.
  - A route-module convention where a route module answers whether it handled a request, so the dispatcher does not grow per route.
  - Moving the existing `/run` endpoint onto that convention unchanged.
- Out:
  - Any behavioural change to serving, to the payload, or to the closed command set of `adr_007`.
  - The open/reveal route itself, which `req_009` owns.

# Acceptance criteria
- AC1: Payload construction, HTTP serving and host interaction are in separate modules.
- AC2: Adding a route does not require editing the dispatching module.
- AC3: `/run` behaves identically, including its token check, its single-flight guard and its refusals.

# AC Traceability
- request-AC9 -> This backlog slice. Proof: AC1: Payload construction, HTTP serving and host interaction are in separate modules.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_011_a_viewer_that_stays_current_and_a_codebase_that_stays_divisible`
- Architecture decision(s): (none yet)
- Request: `req_010_make_the_viewer_refresh_itself_and_give_the_code_a_module_structure_that_holds`
- Primary task(s): `task_024_deliver_the_live_viewer_and_the_module_structure`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.
