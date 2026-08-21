"""Host side of meshanvil. Standard library only, and never imports bpy.

The engine side lives in meshanvil_engine/ and runs inside Blender or FreeCAD.
The two share a schema, not a module -- see adr_004_target_technology_and_process_model.
"""
VERSION = "0.1.0"
SCHEMA_VERSION = 1
