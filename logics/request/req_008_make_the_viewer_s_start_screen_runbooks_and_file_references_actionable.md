## req_008_make_the_viewer_s_start_screen_runbooks_and_file_references_actionable - Make the viewer's start screen, runbooks and file references actionable
> From version: 0.1.0
> Schema version: 1.0
> Status: Draft
> Understanding: 90%
> Confidence: 85%
> Complexity: High
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.

# AI Context
- Summary: (unfilled: replace before this doc is used)
- Keywords: viewer, start, screen, runbooks, file, references, actionable
- Use when: (unfilled: replace before this doc is used)
- Skip when: (unfilled: replace before this doc is used)

# Needs
- The two hand-modelled demonstration assets live under the gitignored logics/external/modeles-3D/ -- fine for a personal machine, but the project itself has nowhere committed to keep them, so a fresh clone (or CI) never sees them.
- The start screen's template cards show commands as plain, uncopiable-looking text with no way to run them, even when the page is served and could run some of them for real; and its three-column layout overflows its own modal on at least one screen width, the Environment column's long paths pushing past the right edge.
- Opening the File menu, then clicking 'Start screen', leaves the File dropdown open and visible behind the splash modal it just opened -- a menu-closing check exists for clicks outside a menu, but the click that opens the splash originates from inside the menu, so that check never runs. (Fixed inline this session, in viewer.js's showSplash -- kept here as a Done slice so the whole pass has one record.)
- A report's render panel and its Artefact section both show a ready-to-run 'blender <path>' command and a written file's path as plain selectable text, never as a button; the same is true of every other file path the viewer prints (runbook references, doc links, project paths in the Environment panel).
- The runbook workspace's right-hand content pane renders a runbook's Markdown source as raw text -- headings, bullet lists and code fences all show their literal '##', '-' and backtick characters instead of being formatted.
- The vehicle demonstration's glass panes (windshield and side/rear windows, thin single-quad Plane objects in the source asset) appear to be progressively lost across the demo chain's own operations -- not yet root-caused to a specific step.

# Context
- adr_007 deliberately closed the set of commands a served page may run (list, doctor, prune) to a fixed, non-destructive set; build_demo_chain.sh and build_figurine_chain.sh are destructive by their own documented intent ('ponytail: destructive on this demonstration's project') and rebuild a whole sibling project from scratch, so adding them to that closed set is an architecture-level decision, not a UI tweak -- surfaced here for a decision, not pre-decided.
- A file:// page has no server to reach and can only ever offer copy-to-clipboard for a command; an 'Open in Blender' affordance on a report's own artefact is a different, narrower case -- opening a local application on a local file the report already names, which a file:// page can offer via a plain file:// or blender:// style link without needing the /run endpoint at all, worth checking before assuming this needs the served-only path too.
- Markdown rendering has to stay dependency-free like the rest of the viewer (adr_003/adr_004's no-framework, no-build-step stance) -- a small hand-rolled renderer covering headings, lists, code fences and links is in scope; pulling in a Markdown library is not.
- The vehicle asset's glass panes are single-quad planes with very little volume of their own; scan_defects' coincident-duplicate removal, solidify's wall-or-skip decision, and voxel_remesh's shell-size floor are the three most likely places a nearly-zero-volume shell gets folded into another object or dropped outright -- named as starting points, not a diagnosis.

# Acceptance criteria
- AC1: Both hand-modelled assets are committed in the repository at a path outside logics/external/ (fixtures/ or equivalent), and both build scripts default to that committed copy first, ahead of the gitignored local one and the from-primitives generator.
- AC2: The start screen's layout stays within its own modal at common desktop widths -- no column's content pushes past the modal's right edge -- verified by a rendered screenshot, not by inspection of the CSS alone.
- AC3: A decision is recorded (a new or amended ADR, or an explicit non-goal) on whether the start screen's demo/figurine template commands become runnable from a served page, and the start screen matches whatever that decision is -- either real run buttons wired through an extended, still-closed command set, or the copy-to-clipboard behaviour kept deliberately and explained in the UI rather than left looking broken.
- AC4: Every report-owned file path the viewer prints (the render panel's 'Open in Blender' command, the Artefact section's written-file path, runbook references, doc links) is a real clickable control -- a button that copies or runs per the file://-vs-served rule already established, or a link that opens the file directly where the platform allows it -- not plain unstyled text.
- AC5: The runbook workspace renders a runbook's Markdown body as formatted HTML (headings, lists, code fences, links at minimum), with no literal Markdown syntax characters visible, using no new dependency.
- AC6: The File-menu-stays-open-behind-the-splash defect is fixed and covered by the same viewer smoke suite so it cannot silently return.
- AC7: The vehicle demonstration's glass-pane loss is root-caused to a specific operation and either fixed (the panes survive the full chain) or, if keeping them intact is not achievable without weakening a real lesson the chain teaches, documented honestly in the build script's comments and README -- not left unexplained.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_009_a_viewer_that_acts_on_what_it_shows_not_just_displays_it`
- Architecture decision(s): (none yet)

# References
- viewer/index.html
- viewer/viewer.js
- viewer/viewer.css
- meshanvil/viewer.py
- logics/external/modeles-3D/base_meshanvil_vehicle.blend
- logics/external/modeles-3D/base_meshanvil_figurine.blend
- tools/build_demo_chain.sh
- tools/build_figurine_chain.sh
- adr_007

# Backlog
- `item_036_commit_the_two_hand_modelled_demo_assets_as_project_fixtures`
- `item_037_fix_the_start_screen_s_layout_overflow_and_decide_its_command_affordance`
- `item_038_make_report_file_paths_and_commands_into_real_clickable_controls`
- `item_039_render_runbook_markdown_as_formatted_content`
- `item_040_root_cause_the_vehicle_demonstration_s_disappearing_glass_panes`
