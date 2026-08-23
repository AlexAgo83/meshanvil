"""meshanvil <command>. One way in, whoever is typing -- a person, Claude or Codex."""
from __future__ import annotations
import argparse, contextlib, io, json, sys

from . import VERSION, demo, doctor, engines, logics_bridge, manifests, paths, prune, runner, viewer
from .i18n import t

ARGPARSE = {
    "usage: ": t("cli.usage"),
    "positional arguments": t("cli.positional_arguments"),
    "options": t("cli.options"),
    "show this help message and exit": t("cli.help"),
    "show program's version number and exit": t("cli.version_help"),
}


def print_json(data: dict) -> None:
    print(json.dumps(data, indent=1))


def colour(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if sys.stdout.isatty() else text


def welcome() -> str:
    name = colour("meshanvil", "1;38;5;214")
    command = "meshanvil view"
    return "\n".join((
        f"{name} {VERSION}",
        t("cli.welcome.tagline"),
        "",
        t("cli.welcome.next"),
        f"  {colour(command, '38;5;75')}{' ' * (24 - len(command))} {t('cli.welcome.view')}",
        f"  {'meshanvil demo':<24} {t('cli.welcome.demo')}",
        f"  {'meshanvil init .':<24} {t('cli.welcome.init')}",
        f"  {'meshanvil doctor':<24} {t('cli.welcome.doctor')}",
        f"  {'meshanvil list':<24} {t('cli.welcome.list')}",
        "",
        t("cli.welcome.help"),
    ))


def build_parser() -> argparse.ArgumentParser:
    argparse._ = lambda text: ARGPARSE.get(text, text)
    parser = argparse.ArgumentParser(prog="meshanvil", description=t("cli.description"))
    parser.add_argument("--version", action="version", version=f"meshanvil {VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)
    listing = sub.add_parser("list", help=t("cli.list.help"))
    listing.add_argument("--json", action="store_true", help=t("cli.json"))
    started = sub.add_parser("init", help=t("cli.init.help"))
    started.add_argument("directory", nargs="?", default=".")
    setup = sub.add_parser("doctor", help=t("cli.doctor.help"))
    setup.add_argument("--json", action="store_true", help=t("cli.json"))
    demonstration = sub.add_parser("demo", help=t("cli.demo.help"))
    demonstration.add_argument("subject", nargs="?", choices=sorted(demo.SUBJECTS), default="figure")
    run = sub.add_parser("run", help=t("cli.run.help"))
    run.add_argument("operation")
    run.add_argument("target")
    run.add_argument("--set", action="append", default=[], metavar="NAME=VALUE",
                     help=t("cli.run.set"))
    run.add_argument("--from", dest="parent", default=None, metavar="ID",
                     help=t("cli.run.from"))
    run.add_argument("--evidence", metavar="TASK:AC", help=t("cli.run.evidence"))
    run.add_argument("--json", action="store_true", help=t("cli.json"))
    show = sub.add_parser("view", help=t("cli.view.help"))
    show.add_argument("--serve", action="store_true",
                      help=t("cli.view.serve"))
    show.add_argument("--file", action="store_true", help=t("cli.view.file"))
    show.add_argument("--no-open", action="store_true", help=t("cli.view.no_open"))
    runbook = sub.add_parser("runbook", help=t("cli.runbook.help"))
    runbook.add_argument("chain")
    pruning = sub.add_parser("prune", help=t("cli.prune.help"))
    pruning.add_argument("--keep", type=int, default=3)
    pruning.add_argument("--dry-run", action="store_true")
    pruning.add_argument("--json", action="store_true", help=t("cli.json"))
    return parser


def show_list(json_mode: bool = False) -> int:
    found = manifests.discover()
    if json_mode:
        print_json({"ok": True, "operations": found})
        return runner.EXIT_OK
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
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print(welcome())
        return runner.EXIT_OK
    arguments = build_parser().parse_args(argv)
    if arguments.command == "list":
        return show_list(arguments.json)
    if arguments.command == "init":
        root, fresh = paths.initialise(arguments.directory)
        # Literal keys: the i18n check reads the source, and a key hidden behind a
        # conditional reads as unused right up until a locale drops it.
        if fresh:
            print(t("cli.project.made", name=paths.name(root), path=root))
        else:
            print(t("cli.project.already", name=paths.name(root), path=root))
        return runner.EXIT_OK
    if arguments.command == "doctor":
        active, rule = paths.resolve()
        result = doctor.check(active)
        if arguments.json:
            print_json({"ok": result["ok"], "project": {
                "name": paths.name(active), "path": str(active), "resolved_by": rule}, "doctor": result})
            return runner.EXIT_OK if result["ok"] else runner.EXIT_REFUSED
        print(t("cli.project.where", name=paths.name(active), path=active, rule=rule))
        print(json.dumps(result, indent=1))
        return runner.EXIT_OK if result["ok"] else runner.EXIT_REFUSED
    if arguments.command == "demo":
        try:
            return demo.run(arguments.subject)
        except (runner.Refused, engines.EngineMissing) as refusal:
            print(str(refusal).strip("'"), file=sys.stderr)
            return runner.EXIT_REFUSED
    if arguments.command == "view":
        return viewer.view(serve_it=True, open_it=not arguments.no_open, file_it=arguments.file)
    if arguments.command == "runbook":
        root = paths.work_root()
        path, error = logics_bridge.runbook(root, root, arguments.chain)
        if error:
            message = (t("bridge.runbook_unavailable") if error == "unavailable"
                       else t("bridge.runbook_error", reason=error))
            print(message, file=sys.stderr)
            return runner.EXIT_REFUSED
        print(path)
        return runner.EXIT_OK
    if arguments.command == "prune":
        project = paths.work_root()
        dropped, freed = prune.run(project, max(0, arguments.keep), arguments.dry_run)
        if arguments.json:
            print_json({"ok": True, "dry_run": arguments.dry_run, "keep": max(0, arguments.keep),
                        "artefacts": [{"path": str(path.relative_to(project)), "bytes": size}
                                      for path, size in dropped],
                        "count": len(dropped), "bytes": freed})
            return runner.EXIT_OK
        for path, size in dropped:
            verb = t("cli.prune.would") if arguments.dry_run else t("cli.prune.deleted")
            print(t("cli.prune.item", path=path.relative_to(project), bytes=size, verb=verb))
        print(t("cli.prune.total", count=len(dropped), bytes=freed))
        return runner.EXIT_OK
    given = {}
    for pair in arguments.set:
        if "=" not in pair:
            message = t("cli.set.malformed", pair=pair)
            if arguments.json:
                print_json({"ok": False, "exit_code": runner.EXIT_REFUSED, "error": message})
                return runner.EXIT_REFUSED
            print(message, file=sys.stderr)
            return runner.EXIT_REFUSED
        name, value = pair.split("=", 1)
        given[name] = value
    try:
        if arguments.json:
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                code = runner.run(arguments.operation, arguments.target, given, arguments.parent, arguments.evidence)
            report = stream.getvalue().strip() or None
            print_json({"ok": code == runner.EXIT_OK, "exit_code": code, "report": report})
            return code
        return runner.run(arguments.operation, arguments.target, given, arguments.parent, arguments.evidence)
    except (runner.Refused, engines.EngineMissing, KeyError) as refusal:
        message = str(refusal).strip("'")
        if getattr(arguments, "json", False):
            print_json({"ok": False, "exit_code": runner.EXIT_REFUSED, "error": message})
            return runner.EXIT_REFUSED
        print(message, file=sys.stderr)
        return runner.EXIT_REFUSED


if __name__ == "__main__":
    sys.exit(main())
