"""Engine side: imported inside Blender or FreeCAD, never by the host.

Reached by path, not by installation: the runner puts the repository root in the job and the
operation inserts it on sys.path. See adr_004_target_technology_and_process_model.
"""
