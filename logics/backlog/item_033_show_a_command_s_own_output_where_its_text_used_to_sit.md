## item_033_show_a_command_s_own_output_where_its_text_used_to_sit - Show a command's own output where its text used to sit
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Low
> Theme: Viewer parity
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# AI Context
- Summary: Wires the three in-scope menu rows to the run endpoint when the page detects it was opened via --serve, showing real stdout/stderr/exit code in place of the copy flash; a file:// page and the two out-of-scope rows keep copying exactly as shipped this session.
- Keywords: served vs file detection, command output, copy-to-clipboard fallback
- Use when: changing what a menu row does with a command's result, or which rows are wired to execution.
- Skip when: the change is server-side only -- the endpoint itself, its token, or its concurrency guard.

# Problem
- The menu's command rows currently only copy their text to the clipboard, on every kind of page.
- A page opened from `file://` has no server to ask and must keep doing exactly that.
- A page opened via `--serve` does have a server now, but nothing on the page knows to use it instead.

# Scope
- In:
  - Detecting whether the page was opened from `--serve` (location.protocol) or from a plain file, once, at load.
  - On a served page, the three in-scope command rows call the run endpoint instead of copying, and show stdout, stderr and exit code where the command text was.
  - On a file:// page, and for `Refresh viewer` / `Create a runbook <report-id>` on any page, the existing copy-to-clipboard behaviour is unchanged.
- Out:
  - Any visual redesign of the menu beyond showing a result in place of, or beside, the command.
  - Streaming partial output; the full result arrives once the subprocess finishes.

# Acceptance criteria
- AC1: A served page running List operations, Check setup or Preview pruning shows the real stdout/stderr/exit code, not the copy-to-clipboard flash.
- AC2: The same rows on a file:// page still only copy to the clipboard, byte-for-byte the behaviour shipped this session.
- AC3: `Refresh viewer` and `Create a runbook <report-id>` copy on every kind of page, served or not.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: A served page running List operations, Check setup or Preview pruning shows the real stdout/stderr/exit code, not the copy-to-clipboard flash.
- request-AC5 -> This backlog slice. Proof: AC2: The same rows on a file:// page still only copy to the clipboard, byte-for-byte the behaviour shipped this session.

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
