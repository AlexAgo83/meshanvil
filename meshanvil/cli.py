"""meshanvil <command>. One way in, whoever is typing -- a person, Claude or Codex."""
from __future__ import annotations
import argparse, sys

from . import VERSION, engines, manifests, runner, viewer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="meshanvil", description=__doc__)
    parser.add_argument("--version", action="version", version=f"meshanvil {VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="the operations found, and what each one takes")
    run = sub.add_parser("run", help="run one operation and write its report")
    run.add_argument("operation")
    run.add_argument("target")
    run.add_argument("--set", action="append", default=[], metavar="NAME=VALUE",
                     help="a parameter of the operation; repeatable")
    run.add_argument("--from", dest="parent", default=None, metavar="ID",
                     help="declare the parent report instead of deriving it from the fingerprint")
    show = sub.add_parser("view", help="build the viewer over the reports and open it")
    show.add_argument("--serve", action="store_true",
                      help="serve it on 127.0.0.1 instead, for auto-refresh while a chain runs")
    show.add_argument("--no-open", action="store_true", help="build it without opening a browser")
    return parser


def show_list() -> int:
    found = manifests.discover()
    if not found:
        print("no operation found. An operation is a script plus a <script>.op.json beside it.")
        return runner.EXIT_OK
    for name, manifest in sorted(found.items()):
        params = ", ".join(f"{p['name']}={p.get('default')}" for p in manifest.get("params", []))
        print(f"{name:22} {manifest['engine']:8} {manifest['kind']:11} {manifest['summary']}")
        if params:
            print(f"{'':22} {params}")
    return runner.EXIT_OK


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    if arguments.command == "list":
        return show_list()
    if arguments.command == "view":
        return viewer.view(serve_it=arguments.serve, open_it=not arguments.no_open)
    given = {}
    for pair in arguments.set:
        if "=" not in pair:
            print(f"--set expects NAME=VALUE, got {pair}", file=sys.stderr)
            return runner.EXIT_REFUSED
        name, value = pair.split("=", 1)
        given[name] = value
    try:
        return runner.run(arguments.operation, arguments.target, given, arguments.parent)
    except (runner.Refused, engines.EngineMissing, KeyError) as refusal:
        print(str(refusal).strip("'"), file=sys.stderr)
        return runner.EXIT_REFUSED
