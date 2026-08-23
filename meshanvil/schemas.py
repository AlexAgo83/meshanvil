"""Machine-readable CLI contracts. Descriptive, not a runtime validator."""
from __future__ import annotations

from . import runner

ERROR_CODES = [
    "unknown_operation",
    "missing_source_file",
    "engine_missing",
    "target_busy",
    "invalid_parameter",
    "malformed_set",
    "unreadable_input_format",
    "work_unavailable",
    "report_not_found",
    "ambiguous_report_id",
    "malformed_report",
    "operation_failed",
    "no_report",
]


def all_schemas() -> dict:
    return {
        "report": {
            "required": ["schema_version", "id", "operation", "status", "input", "output", "tool"],
            "optional": ["params", "measurements", "findings", "warnings", "renders", "links"],
            "status": ["ok", "failed"],
            "input": {"path": "string", "sha256": "string"},
            "output": {"path": "string", "state": "present|pruned|missing", "sha256": "string"},
        },
        "operation": {
            "required": ["operation", "engine", "kind", "script", "summary_key"],
            "optional": ["params", "accepts", "opens_target"],
            "engines": ["blender", "freecad"],
            "parameter": {"required": ["name", "type", "default"], "optional": ["unit"],
                          "types": ["int", "float", "str", "bool"]},
        },
        "cli": {
            "success": {"ok": True, "exit_code": "integer on commands that can refuse/fail"},
            "error": {"ok": False, "exit_code": "integer",
                      "error": {"code": "stable string", "message": "localized human text"}},
            "exit_codes": {"ok": runner.EXIT_OK, "failed": runner.EXIT_FAILED,
                           "refused": runner.EXIT_REFUSED, "no_report": runner.EXIT_NO_REPORT},
            "error_codes": ERROR_CODES,
        },
    }
