## run_010_verify_that_a_command_did_what_it_appeared_to_do - Verify that a command did what it appeared to do
> Status: Active
> Category: other
> Verified: 2026-08-21 (six silent failures collected in one session, each one caught by a proof line rather than by the command's own output); 2026-08-22 added a seventh and an eighth, both from headless-browser smokes rather than a shell
> Related request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
> Related backlog: (none yet)
> Related task: `task_001_deliver_the_reviewable_operation_loop`
> Reminder: Update status, category, verification, and linked refs when you edit this doc.
> Indicators reviewed: 2026-08-22 17:29:43

# Trigger
- An agent is driving work through a shell, and the next step depends on the previous one having done what it said.
- A conclusion is about to be drawn from a command's output: "nothing was found", "it did nothing", "the platform does not support it".

# Prerequisites
- Know which shell is actually interpreting the line. On macOS an interactive agent shell is usually zsh, and zsh differs from bash on exactly the cases below.
- Know how many shells a remote command crosses. Four is normal for a Windows host with WSL: local shell, ssh, `cmd.exe`, then `bash -lic`.

# Procedure
1. **Make every destructive or preparatory step print a proof line.** Not the command's own output: a separate observation of the state it was supposed to produce. `rm` then `ls | wc -l`. A cleanup nobody verified is a cleanup that may not have run.
2. **Never let a glob be the only thing standing between you and a wrong conclusion.** In zsh a pattern that matches nothing aborts the whole command line with `no matches found`, so `rm -f a/*.x b/*.y` deletes nothing at all when only the second pattern is empty. Use `find <dir> -name '<pattern>' -delete`, which is silent on zero matches and identical on both shells.
3. **Do not pipe a command whose exit code you are about to read.** `cmd | grep x; echo $?` reports grep's status, not the command's. Run it, read `$?`, then filter separately.
4. **Quote every variable, and assume no word splitting.** zsh does not split an unquoted parameter into words, so `$cmd` holding `run op file` is passed as one argument. A loop built that way produced four exit codes of zero in a tenth of a second and looked like four successful runs.
5. **Through more than two shells, inline the value instead of naming it.** A variable expanded across ssh, `cmd.exe`, `wsl.exe` and `bash -lic` collapsed to empty, so the command ran as `"" --version`. The conclusion drawn -- that the Windows binary does nothing when called from Linux -- was false, and the retest with the path written literally worked on the first attempt.
6. **Check the regex dialect before trusting a gate that found nothing.** `git grep -E` is POSIX ERE, where `\b` is undefined: a word-boundary anchor silently matches nothing on macOS. Spell edges out as `(^|[^A-Za-z])` and `([^a-z]|$)`.
7. **Test a gate in both directions, every time.** Feed it a line that must fail and confirm it fails, then remove the line and confirm it passes. A gate that has only ever returned "clean" has not been shown to be a gate.
8. **A check that cannot pass in its own harness is not proof the thing it checks is broken.** A headless-Chrome smoke asserting on `navigator.clipboard.writeText` and on `document.execCommand("copy")` got `NotAllowedError: Document is not focused` and `execCommand=false` from both, on a feature that works the moment a person clicks it in a real, focused tab. The env lacks focus and clipboard permission by construction, not because the code regressed. Assert what the harness can actually prove -- the button exists, is a real `<button>`, and clicking it never throws -- not the part of the behaviour the harness cannot grant.
9. **`--virtual-time-budget` is not a reason to drop it against a live server -- it is why the timers waiting on that server's response ever fire.** A smoke against a real `--serve` subprocess omitted the flag on the theory that virtualised time would fight a real network round trip; `--dump-dom` then returned the page exactly as it loaded, before the click handler's `fetch` had a chance to resolve, because Chrome dumps at the load event and does not wait for pending JS timers on its own. The flag does not block real sockets, it advances the clock so the `setTimeout` polling loop waiting on the response actually runs before the dump. Verified by adding it back at 5s and watching the same assertion pass.

# Verification
- After a cleanup: count what remains, do not assume. `ls work/ops/*.json | wc -l`.
- After a remote command: read something written on the far side, not the exit code. A command that never ran and a command that ran without effect both exit 0.
- After changing a pattern in a check: run the corpus of known positives past it. Four out of five caught is a failing pattern, and only an explicit list shows which one escaped.
- When a measurement contradicts an action that was supposed to change it: suspect the measurement first. In Blender, `object.bound_box` is a cache that stays stale until the depsgraph updates, and reading it after a mesh edit reports the geometry from before the edit.
- Before asserting on a browser API in a headless smoke: check what the harness itself can grant (focus, permissions, a real user gesture) and assert only up to that boundary.
- Before dropping a Chrome timing flag against a live server on a theoretical conflict: try it with the flag first. `--dump-dom` proves nothing about work still pending in a timer when the dump was taken without one.

# Rollback
- Nothing here writes. The cost of the mistakes is wasted reasoning, and the recovery is re-running the step with a proof line attached.

# Limits to state, not to hide
- These are the traps met in one session on one machine; the class is larger. The transferable rule is the one they share, not the list: **a command that printed nothing is not a command that found nothing.**
- Proof lines cost a round trip each. On a tight loop, verify at the boundaries -- after a cleanup, before a conclusion -- rather than after every step.
- An agent that adds a proof line to every command becomes unreadable. The discipline applies to steps whose failure would be silent, which is a much smaller set than "all of them".

# References
- The same discipline applied to geometry: `run_006_turn_a_cad_assembly_into_a_printable_solid`, where the bounding box was the only check that spoke
- The platform facts this was learned on: `adr_004_target_technology_and_process_model`
- Related request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Related task: `task_001_deliver_the_reviewable_operation_loop`
