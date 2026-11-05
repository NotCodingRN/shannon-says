"""Command-line entry point."""
from __future__ import annotations

import argparse
import random
import sys

from shannon_says import __version__
from shannon_says.units import UnitError

QUIPS = [
    "Not a bit more.",
    "The channel has spoken.",
    "Noise always gets a vote.",
    "Bandwidth is temporary, log2 is forever.",
    "Error-free, in theory. Theory is great.",
    "Coding gain sold separately.",
]


def say(line: str, quiet: bool) -> None:
    print(line)
    if not quiet:
        print(f"Shannon says: {random.choice(QUIPS)}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="shannon-says", description="Tiny comms-engineering calculator.")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("-q", "--quiet", action="store_true", help="numbers only, no commentary")
    p.add_subparsers(dest="cmd", metavar="COMMAND")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 0
    try:
        args.func(args)
    except UnitError as e:
        print(f"shannon-says: {e}", file=sys.stderr)
        return 2
    return 0
