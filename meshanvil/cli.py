"""meshanvil <command>. One way in, whoever is typing -- a person, Claude or Codex."""
from __future__ import annotations
import argparse, json, sys

from . import VERSION, doctor, engines, logics_bridge, manifests, runner, viewer
from .i18n import t

ARGPARSE = {
    "usage: ": t("cli.usage"),
    "positional arguments": t("cli.positional_arguments"),
    "options": t("cli.options"),
    "show this help message and exit": t("cli.help"),
    "show program's version number and exit": t("cli.version_help"),
}


def build_parser() -> argparse.ArgumentParser:
    argparse._ = lambda text: ARGPARSE.get(text, text)
    parser = argparse.ArgumentParser(prog="meshanvil", description=t("cli.description"))
    parser.add_argument("--version", action="version", version=f"meshanvil {VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help=t("cli.list.help"))
    sub.add_parser("doctor", help=t("cli.doctor.help"))
    run = sub.add_parser("run", help=t("cli.run.help"))
    run.add_argument("operation")
    run.add_argument("target")
    run.add_argument("--set", action="append", default=[], metavar="NAME=VALUE",
                     help=t("cli.run.set"))
    run.add_argument("--from", dest="parent", default=None, metavar="ID",
                     help=t("cli.run.from"))
    run.add_argument("--evidence", metavar="TASK:AC", help=t("cli.run.evidence"))
    show = sub.add_parser("view", help=t("cli.view.help"))
    show.add_argument("--serve", action="store_true",
                      help=t("cli.view.serve"))
    show.add_argument("--no-open", action="store_true", help=t("cli.view.no_open"))
    runbook = sub.add_parser("runbook", help=t("cli.runbook.help"))
    runbook.add_argument("chain")
    return parser


def show_list() -> int:
    found = manifests.discover()
    if not found:
        print(t("list.empty"))
        return runner.EXIT_OK
    for name, manifest in sorted(found.items()):
        params = ", ".join(f"{p['name']}={p.get('default')}" for p in manifest.get("params", []))
        print(f"{name:22} {manifest['engine']:8} {manifest['kind']:11} {t(manifest['summary_key'])}")
        if params:
            print(f"{'':22} {params}")
    return runner.EXIT_OK


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    if arguments.command == "list":
        return show_list()
    if arguments.command == "doctor":
        result = doctor.check(manifests.root())
        print(json.dumps(result, indent=1))
        return runner.EXIT_OK if result["ok"] else runner.EXIT_REFUSED
    if arguments.command == "view":
        return viewer.view(serve_it=arguments.serve, open_it=not arguments.no_open)
    if arguments.command == "runbook":
        path, error = logics_bridge.runbook(manifests.root(), arguments.chain)
        if error:
            message = (t("bridge.runbook_unavailable") if error == "unavailable"
                       else t("bridge.runbook_error", reason=error))
            print(message, file=sys.stderr)
            return runner.EXIT_REFUSED
        print(path)
        return runner.EXIT_OK
    given = {}
    for pair in arguments.set:
        if "=" not in pair:
            print(t("cli.set.malformed", pair=pair), file=sys.stderr)
            return runner.EXIT_REFUSED
        name, value = pair.split("=", 1)
        given[name] = value
    try:
        return runner.run(arguments.operation, arguments.target, given, arguments.parent, arguments.evidence)
    except (runner.Refused, engines.EngineMissing, KeyError) as refusal:
        print(str(refusal).strip("'"), file=sys.stderr)
        return runner.EXIT_REFUSED
