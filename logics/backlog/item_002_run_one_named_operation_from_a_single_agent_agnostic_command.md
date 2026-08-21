## item_002_run_one_named_operation_from_a_single_agent_agnostic_command - Run one named operation from a single agent-agnostic command
> From version: 1.0.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# AI Context
- Summary: One command that resolves the Blender binary, runs a named operation headless on a target file, refuses to write to work/in/, and prints the report path.
- Keywords: runner command, operation discovery, headless invocation, source protection, agent-agnostic
- Use when: Changing how an operation is launched, or what an agent has to know to launch one.
- Skip when: Designing the report contents (item_001) or the viewer (item_003); packaging an MCP server, which this slice excludes.

# Problem
- Running an operation today means knowing the Blender binary path, the -b and -P flags, which file to open and which script to pass.
- That invocation is what every agent has to reconstruct, and it is where a wrong file or a missing copy silently ruins the work.
- Nothing enforces that an operation runs on a copy rather than on a source under work/in/.

# Scope
- In:
  - A meshanvil command taking an operation name and a target file, resolving the Blender binary, running it headless and returning the report path.
  - Operation discovery from pipeline/ and tools/, so adding a script adds an operation without registering it anywhere.
  - A refusal to write to work/in/, with a clear message naming the copy to work on instead.
  - A list mode printing the available operations and what each one needs.
- Out:
  - Chaining several operations in one invocation.
  - Any MCP server or agent plugin packaging, which is its own decision later.
  - Installing or locating Blender for the user beyond an environment variable and the documented default.

# Acceptance criteria
- AC1: One command runs a named operation on a given file and prints the path of the report it wrote.
- AC2: The same command works unchanged whether it is typed by hand or run by an agent; nothing in its interface depends on the runtime.
- AC3: Pointing the command at a file under work/in/ is refused with a message naming what to do instead.
- AC4: The Blender binary comes from an environment variable when set, and from the documented default otherwise.

# AC Traceability
- request-AC4 -> This backlog slice. Proof: AC1: One command runs a named operation on a given file and prints the path of the report it wrote.
- request-AC8 -> This backlog slice. Proof: AC2: The same command works unchanged whether it is typed by hand or run by an agent; nothing in its interface depends on the runtime.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_001_reviewable_agent_driven_3d_operations`
- Architecture decision(s): (none yet)
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Primary task(s): `task_001_deliver_the_reviewable_operation_loop`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.
