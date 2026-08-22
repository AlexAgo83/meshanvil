## req_006_let_the_viewer_run_the_commands_it_already_shows_when_it_is_served - Let the viewer run the commands it already shows, when it is served
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Complexity: Medium
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 17:28:44

# AI Context
- Summary: adr_003 refused to let the viewer execute anything and priced the reversal; this request pays that price for a closed set of three argument-free commands, served locally with a per-launch token and one command running at a time, while a plain file:// page stays copy-only.
- Keywords: served viewer, local server execution, per-launch token, adr_003 supersession, closed command set
- Use when: adding or changing what a served viewer page can run, or revisiting the security boundary around it.
- Skip when: the change is about copy-to-clipboard on a file:// page, or about running a command outside the closed set.

# Needs
- adr_003 refused execution on purpose and priced the reversal: a local server with authentication, a job model, and a decision about concurrent access to a file Blender may already hold. That price is now being paid deliberately, not discovered as a surprise later.
- The menu bar already shows the exact command for List operations, Check setup and Preview pruning, and this session made that text copyable to the clipboard. A person still has to leave the page and paste it into a terminal to see the result.
- `meshanvil view --serve` already runs an opt-in `http.server` on 127.0.0.1, port 0, for auto-refresh (adr_004). It currently serves `work/` read-only; nothing posts to it.
- A page opened from `file://` has no server behind it at all and can never run anything -- the copy-to-clipboard behaviour just shipped has to stay its only option there.
- `Refresh viewer` would restart the very server handling the request that triggers it, and `Create a runbook <report-id>` shows a placeholder id, not a real one -- neither is safe to wire to real execution in this slice.

# Context
- The runner already refuses a busy target (target_busy) and already serialises identity allocation per project; this request does not re-implement that, it only serialises its own subprocess calls so two clicks on the same button cannot race each other.
- The three commands in scope take no destructive action and no operator-supplied argument: they are the same closed set already printed in the menu, never a string typed on the page.
- The port is already random per launch (port 0); a per-launch token embedded in the page's own data.js is the authentication adr_003 named, sized to a single-operator localhost tool rather than a login system.

# Acceptance criteria
- AC1: Opened via `meshanvil view --serve`, each of List operations, Check setup and Preview pruning runs from its menu row and shows its stdout, stderr and exit code in the page; opened from a plain file, the same rows still only copy the command, exactly as they do today.
- AC2: The server refuses to run anything unless the request carries the exact per-launch token embedded in that session's data.js; a missing or mismatched token is refused before any subprocess starts.
- AC3: The server accepts only one of the three fixed named commands; any other value is refused, and nothing the page sends can become part of the command line.
- AC4: A second run request arriving while one is still executing is refused, not queued, and the first request's result is still returned to whoever asked for it.
- AC5: `Refresh viewer` and `Create a runbook <report-id>` stay copy-only in this slice; the cut is recorded as a backlog item rather than silently dropped.
- AC6: adr_003 is marked Superseded by a new ADR that records the security boundary chosen -- localhost-only, per-launch token, one command at a time, a closed command set -- and states why it satisfies the price adr_003 named rather than reopening the question from zero.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_007_a_served_viewer_that_can_run_what_it_already_shows`
- Architecture decision(s): `adr_007_let_the_served_viewer_execute_a_closed_command_set` (supersedes `adr_003_the_viewer_reads_the_command_acts` in part)

# References
- meshanvil/viewer.py
- viewer/viewer.js
- viewer/index.html
- bin/meshanvil
- logics/architecture/adr_003_the_viewer_reads_the_command_acts.md
- logics/architecture/adr_004_target_technology_and_process_model.md

# Backlog
- `item_032_run_a_closed_set_of_commands_from_the_served_viewer_s_own_server`
- `item_033_show_a_command_s_own_output_where_its_text_used_to_sit`
