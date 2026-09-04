from __future__ import annotations

import argparse
from pathlib import Path

from .config import AlinaConfig
from .spec.compiler import SpecCompileError, SpecCompiler


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="alinacoder")
    sub = parser.add_subparsers(dest="command", required=True)
    spec = sub.add_parser("spec-compile", help="validate the active v0.2 normative spec")
    spec.add_argument("--root", default=".")
    spec.add_argument("--manifest", default="docs/superpowers/specs/2026-09-04-alinacoder-v0.2-normative-manifest.json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    AlinaConfig().validate()
    if args.command == "spec-compile":
        root = Path(args.root).resolve()
        try:
            result = SpecCompiler(root).compile(root / args.manifest)
        except SpecCompileError as exc:
            print(f"SPEC_INVALID: {exc}")
            return 2
        print(f"SPEC_VALID invariants={len(result.invariants)} documents={len(result.validated_documents)}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
