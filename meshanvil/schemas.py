"""Machine-readable CLI contracts. Descriptive, not a runtime validator."""
from __future__ import annotations

from . import runner

# Every code a JSON command can put in `error.code`. A declared list that omits one is worse
# than no list: an agent branches on it and never sees the case coming. `check_error_codes`
# in scripts/selfcheck.py drives the refusals and fails if one is emitted from outside here.
ERROR_CODES = [
    "unknown_operation",
    "missing_source_file",
    "engine_missing",
    "target_busy",
    "invalid_parameter",
    "malformed_set",
    "unreadable_input_format",
    "read_only_source",
    "work_unavailable",
    "setup_refused",
    "report_not_found",
    "ambiguous_report_id",
    "malformed_report",
    "operation_failed",
    "no_report",
    "refused",
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
