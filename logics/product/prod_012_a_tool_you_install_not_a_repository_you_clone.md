## prod_012_a_tool_you_install_not_a_repository_you_clone - A tool you install, not a repository you clone
> Date: 2026-08-23
> Status: Settled
> Related request: `req_011_make_meshanvil_an_installable_tool_instead_of_a_repository_you_clone`
> Related backlog: `item_051_declare_the_package_and_give_the_tool_a_real_entry_point`
> Related task: `task_025_deliver_an_installable_meshanvil`
> Related architecture: (none yet)
> Reminder: Update status, linked refs, scope, decisions, success signals, and open questions when you edit this doc.
> Indicators reviewed: 2026-08-23 02:00:17

# Overview
Turns meshanvil from a source tree that has to be acquired into a command an operator installs once and uses in any project directory, without giving up the working-tree route contributors depend on and without pretending to support a platform nobody measured.

```mermaid
flowchart LR
  idx[Python index] --> inst["Isolated tool install: one command on PATH"]
  inst --> doc["meshanvil doctor: names the engine you still need"]
  doc --> proj["meshanvil init <dir>, then run and view in any project"]
  tree[Working tree] --> rule[One repo-first asset rule]
  pkg[Built package] --> rule
  rule --> assets["manifests, catalogues, viewer bundle, engine package"]
  build[Build] --> verify[Verify the package carries its assets]
  verify -->|missing| fail[Build fails, asset named]
  verify -->|complete| rel["Release: states measured platforms, names the unverified"]
```

# Goals
- Getting the tool is one command, and the only real prerequisite left is the one no packaging can remove.
- The tool finds what it needs by one rule, whether it is running from a checkout or from an installed package.
- A package that is missing part of itself fails at build time, not at an operator's first run.
- What is supported and what is unverified is stated where someone about to install reads it.

# Non-goals
- Publishing through npm; nothing in the runtime is JavaScript and `adr_002` already fixed npm's role.
- A graphical installer, a bundled Blender, or any attempt to hide the engine requirement.
- Actually publishing a release in this pass -- the machinery and the decision, not the act.

# Scope and guardrails
- In: scaffolded request, product, backlog, orchestration task, validation, and handoff context.
- Out: unrelated workflow docs and implementation of generated tasks.

# Key product decisions
- Use structured input as the source of truth for generated docs.
- Keep generated write paths local and repo-bounded.

# Success signals
- Generated docs pass lint and audit without broad manual rewrites.
- Context-pack output can be handed to an implementation agent directly.

# References
- Product back-reference: `item_051_declare_the_package_and_give_the_tool_a_real_entry_point`
- Task back-reference: `task_025_deliver_an_installable_meshanvil`
