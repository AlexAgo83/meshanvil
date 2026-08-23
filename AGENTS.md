@LOGICS.md

# Agent CLI Contract

Use JSON mode for automation: `meshanvil status --json`, `meshanvil schema --json`,
`meshanvil list --json`, `meshanvil doctor --json`, `meshanvil run ... --json`,
and `meshanvil reports ... --json`.

Start with `status --json`, then `schema --json`, then discover operations before
running one. Treat reports as the record: read them through `reports --json`,
`reports --latest --json`, or `reports <id> --json` instead of parsing stdout.

Exit codes are stable: `0` ok, `1` operation failed, `2` refused before or at the
boundary, `3` engine wrote no report. JSON includes the same code in `exit_code`
when a command can fail or refuse.

Safety rules: never write into `work/in`, do not commit `work/`, and keep client,
source, and local path names out of committed docs. When implementing an active
Logics task, pass evidence with `--evidence TASK:AC`.
