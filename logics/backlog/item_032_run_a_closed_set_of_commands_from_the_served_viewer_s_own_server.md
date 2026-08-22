## item_032_run_a_closed_set_of_commands_from_the_served_viewer_s_own_server - Run a closed set of commands from the served viewer's own server
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# AI Context
- Summary: The --serve server only serves files; this adds one POST endpoint that runs one of three fixed commands as a bin/meshanvil subprocess, gated by a per-launch token and a single-flight lock, and supersedes adr_003 with the ADR that records this exact boundary.
- Keywords: run endpoint, per-launch token, single-flight, closed command set, adr supersession
- Use when: changing the server's authentication, its command set, or its concurrency guard.
- Skip when: the change is only about how the page displays a result, not how the server executes one.

# Problem
- The `--serve` server only serves files; there is no way for the page to ask it to do anything.
- adr_003 named the price of changing that -- authentication, a job model, a concurrency decision -- without paying it, so paying it now needs its own recorded decision, not a quiet code change.
- Nothing today stops a page from sending an arbitrary string if a run endpoint is added without a closed command set and a token.

# Scope
- In:
  - One POST endpoint on the existing `--serve` server that runs one of List operations, Check setup or Preview pruning as a subprocess of `bin/meshanvil`, the same entry point a person would type.
  - A random token generated per server launch, embedded in `data.js`, required on every request to the endpoint.
  - Serialising the endpoint's own subprocess calls so a second request while one runs is refused outright.
  - Superseding adr_003 with a new ADR naming this exact boundary.
- Out:
  - Any command that takes a path, an operation name, or any other operator-supplied value.
  - A queue, retry, or history of past runs.
  - Changing what `--serve` does when no run is requested; file serving is unchanged.

# Acceptance criteria
- AC1: The endpoint runs exactly one of the three fixed commands by name, never a string from the request body.
- AC2: A request without the current per-launch token, or with a stale one from a previous launch, is refused before any subprocess starts.
- AC3: A request that arrives while another is executing is refused immediately; the request already running still returns its result.
- AC4: adr_003 carries a Superseded status pointing at the new ADR, and the new ADR references adr_003's named price and states how each part of it was paid.

# AC Traceability
- request-AC2 -> This backlog slice. Proof: AC1: The endpoint runs exactly one of the three fixed commands by name, never a string from the request body.
- request-AC3 -> This backlog slice. Proof: AC2: A request without the current per-launch token, or with a stale one from a previous launch, is refused before any subprocess starts.
- request-AC4 -> This backlog slice. Proof: AC3: A request that arrives while another is executing is refused immediately; the request already running still returns its result.
- request-AC6 -> This backlog slice. Proof: AC4: adr_003 carries a Superseded status pointing at the new ADR, and the new ADR references adr_003's named price and states how each part of it was paid.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_007_a_served_viewer_that_can_run_what_it_already_shows`
- Architecture decision(s): (none yet)
- Request: `req_006_let_the_viewer_run_the_commands_it_already_shows_when_it_is_served`
- Primary task(s): `task_020_let_the_viewer_run_the_commands_it_already_shows_when_it_is_served`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.
