## run_001_drive_a_live_blender_session_from_the_agent - Drive a live Blender session from the agent
> Status: Active
> Category: other
> Verified: 2026-08-21 (real session, Blender 5.2 LTS on macOS, ~700-object CAD assembly)
> Related request: (none yet)
> Related backlog: (none yet)
> Related task: (none yet)
> Reminder: Update status, category, verification, and linked refs when you edit this doc.
> Indicators reviewed: 2026-08-21 19:47:37

# Trigger
- The operator has a Blender scene open on screen and wants the agent to inspect or modify it live.
- The agent needs to see the result of a 3D operation rather than assume it.
- Not for pure batch work: a .blend to process without interaction goes through headless mode (Procedure, variant B).

# Prerequisites
- Blender installed. On macOS the binary is not on PATH: `/Applications/Blender.app/Contents/MacOS/Blender`.
- The agent can read and write files in the operator's real home directory.
- WARNING: the agent shell's HOME may be redirected (profiles, sandboxes). Check `echo $HOME` against the real home before writing the bridge; bridge paths must be absolute and hardcoded, never `~` or `pathlib.Path.home()`.
- The operator saves the scene before any non-read-only operation: the agent writes into the live session.

# Procedure
1. Write the bridge once per machine, e.g. `<REAL_HOME>/bl_bridge.py`:
   - a callback registered with `bpy.app.timers.register(tick)` returning `0.5`;
   - `tick` compares the `st_mtime` of `<REAL_HOME>/bl_cmd.py` against the last seen value;
   - on change, `exec(compile(...))` its contents with `contextlib.redirect_stdout` into a buffer;
   - write the buffer (plus `traceback.format_exc()` on exception) to `<REAL_HOME>/bl_out.txt`.
2. Ask the operator to arm it: **Scripting** tab, Python Console panel bottom-left, paste
   `exec(open('<REAL_HOME>/bl_bridge.py').read())`. Repeat after every Blender restart.
3. Work loop: the agent writes `bl_cmd.py`, waits, reads `bl_out.txt`. Always end scripts with an explicit `print` that serves as the acknowledgement.
4. To see the scene: `bpy.ops.render.opengl(write_still=True)` inside a `bpy.context.temp_override(window=..., area=..., region=...)` on a `VIEW_3D` area, then read the resulting PNG.
5. Variant B, no open session: `/Applications/Blender.app/Contents/MacOS/Blender -b -P script.py -- /absolute/out.png`.

# Letting the operator point
When a feature has to be located in a dense mesh, geometric filters are often useless: in a
700k-face body, every bounding box drawn around a suspected part also catches the floor
and the panel behind it. Three filter attempts failed to isolate a 20 mm rod.

Ask the operator to place the **3D cursor** on it (`Shift` + right-click) and read
`bpy.context.scene.cursor.location`, then probe outward from that point at increasing radii to
recover the feature's extent. One round trip instead of three. Reading their **selection** works
too, but check `object.mode` first and read through `bmesh.from_edit_mesh` in Edit Mode -- and be
aware a stale selection from an earlier operation looks exactly like a deliberate one, so compare
what is selected against what they said they selected.

# Verification
- First round trip: `print("hello", len(bpy.data.objects))` must come back in `bl_out.txt` within two seconds.
- A Blender-side exception must surface as a traceback in `bl_out.txt`, not as silence. Test that once on purpose.
- The viewport PNG must be read back by the agent, not merely produced. A written file is not a seen image.

# Rollback
- The bridge does not persist: closing Blender disarms it. Otherwise `bpy.app.timers.unregister(tick)`.
- Scene operations stay in Blender's undo stack: `Ctrl+Z` on the operator's side.
- The agent never saves the .blend on its own initiative.

# Pitfalls hit in practice
- Blender ignores the shell cwd: every output path must be absolute, otherwise `Couldn't create directory for file`.
- The timer only fires while Blender's UI ticks. A heavy script (raycast sweeps) can outlast the planned wait: re-read `bl_out.txt` instead of concluding failure.
- Object names from CAD imports carry double spaces, apostrophes and accents. Never retype them: match by substring.
- `view3d.view_axis` names are camera directions, not object sides, and the mapping depends on how the model was exported. In the assembly handled here `LEFT`/`RIGHT` framed the two ends of the object (they look along X) while `FRONT`/`BACK` framed its flanks (they look along Y). Determine the mapping once by rendering, note it, and stop guessing: two wasted renders each time otherwise.
- Round-trip latency is ~0.5 s. For iterative visual placement, see the limit documented in run_002.

# References
- Related request: (none yet)
- Related backlog: (none yet)
- Related task: (none yet)
