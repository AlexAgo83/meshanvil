## item_056_refuse_a_served_viewer_request_that_did_not_come_from_its_own_page - Refuse a served-viewer request that did not come from its own page
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 95%
> Confidence: 90%
> Progress: 90%
> Complexity: Medium
> Theme: Host boundary
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 10:21:31

# AI Context
- Summary: One origin guard ahead of route dispatch, refusing a non-loopback Host or a foreign Origin, plus the SECURITY.md and adr_007 rewrite that makes the documented boundary the real one.
- Keywords: refuse, served, viewer, request, did, not, come, own, page
- Use when: adding or reviewing the check that decides whether the served viewer answers a request at all.
- Skip when: changing how the page obtains run_token, adding CORS headers or a second credential, or altering stable_port.

# Problem
- GET /api/data and the static file work/viewer/data.js both hand out run_token with no token check, and run_token is what gates POST /run and POST /file.
- No route inspects Host, Origin or Referer, so a page in the operator's own browser that resolves a name to 127.0.0.1 reaches the server as a same-origin caller.
- stable_port makes the port a function of the project path rather than a random value, while SECURITY.md still describes a random port and a token embedded only in the generated page.
- work/viewer/server.json, the reuse registry, carries the same token and sits inside the served directory, so a per-route token check would not have closed the read path anyway.

# Scope
- In:
  - A single origin guard in the request handler, applied to every GET and POST before any route dispatch or static file is served, so the reuse registry and data.js are behind it too.
  - The guard reads the port from the bound socket at request time: make_server defaults to port 0 and both scripts/selfcheck.py and tests/test_viewer.py call it that way, so the port argument is not the served port.
  - Refusal of any request whose Host header is absent or names something other than a loopback host, and of any present Origin that is not this server's own.
  - Rewriting the '--serve' section of SECURITY.md and the boundary section of adr_007 to state the port rule, what the token proves, and the cross-origin answer.
  - One selfcheck covering an accepted request and each refused shape, with its pytest wrapper.
- Out:
  - Removing run_token from the payload or changing how the page obtains it; app.js derives its served flag from it and that is a separate decision.
  - CORS response headers, cookies, sessions, or any second credential.
  - Changing stable_port itself, which item on reuse deliberately made stable.

# Acceptance criteria
- AC1: A request carrying Host: evil.example is refused on /api/ping, /api/data, /api/events, /run, /file and a static path, with no route body executed.
- AC2: A request carrying an Origin other than this server's own is refused even when its Host is loopback; a request with no Origin and a loopback Host is served.
- AC3: SECURITY.md and adr_007 name the port rule and the token's actual guarantee, and neither states that the port is random or that the token is unreadable.
- AC4: The guard holds on a server started with port 0, where the served port is known only after the socket is bound.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC4: The guard holds on a server started with port 0, where the served port is known only after the socket is bound.
- request-AC1 -> This backlog slice. Proof: AC1: A request carrying Host: evil.example is refused on /api/ping, /api/data, /api/events, /run, /file and a static path, with no route body executed.
- request-AC2 -> This backlog slice. Proof: AC2: A request carrying an Origin other than this server's own is refused even when its Host is loopback; a request with no Origin and a loopback Host is served.
- request-AC8 -> This backlog slice. Proof: AC3: SECURITY.md and adr_007 name the port rule and the token's actual guarantee, and neither states that the port is random or that the token is unreadable.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_013_a_host_boundary_that_matches_its_own_documentation`
- Architecture decision(s): (none yet)
- Request: `req_013_make_the_served_viewer_prune_and_project_resolution_behave_the_way_they_are_documented`
- Primary task(s): `task_026_close_the_review_findings_on_the_served_viewer_prune_and_project_resolution`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.
