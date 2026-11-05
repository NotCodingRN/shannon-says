"""Command-line entry point."""
from __future__ import annotations

import argparse
import random
import sys

from shannon_says import __version__, core, units
from shannon_says.units import UnitError

QUIPS = [
    "Not a bit more.",
    "The channel has spoken.",
    "Noise always gets a vote.",
    "Bandwidth is temporary, log2 is forever.",
    "Error-free, in theory. Theory is great.",
    "Coding gain sold separately.",
]


def say(lines: list[str], quiet: bool) -> None:
    print("\n".join(lines))
    if not quiet:
        print(f"Shannon says: {random.choice(QUIPS)}")


# ---------------------------------------------------------------- commands
def cmd_capacity(a) -> None:
    bw = units.frequency(a.bandwidth)
    snr = units.ratio_db(a.snr)
    c = core.capacity(bw, snr)
    say([
        f"Bandwidth            {units.pretty_freq(bw)}",
        f"SNR                  {snr:.2f} dB  ({core.db_to_linear(snr):.4g}x)",
        f"Capacity             {units.pretty_rate(c)}",
        f"Spectral efficiency  {core.spectral_efficiency(snr):.3f} bit/s/Hz",
    ], a.quiet)


def cmd_need(a) -> None:
    bw = units.frequency(a.bandwidth)
    rate = units.rate(a.rate)
    snr = core.snr_needed(bw, rate)
    say([
        f"To push {units.pretty_rate(rate)} through {units.pretty_freq(bw)}",
        f"you need at least    {snr:.2f} dB SNR  ({core.db_to_linear(snr):.4g}x)",
    ], a.quiet)


def cmd_db(a) -> None:
    text = a.value.strip()
    low = text.lower()
    if low.endswith("dbm"):
        dbm = units.power_dbm(text)
        lines = [f"{dbm:g} dBm = {core.dbm_to_watts(dbm):.4g} W = {dbm - 30:g} dBW"]
    elif low.endswith("dbw"):
        dbm = units.power_dbm(text)
        lines = [f"{dbm - 30:g} dBW = {core.dbm_to_watts(dbm):.4g} W = {dbm:g} dBm"]
    elif low.endswith("w"):
        dbm = units.power_dbm(text)
        lines = [f"{text} = {dbm:.2f} dBm = {dbm - 30:.2f} dBW"]
    elif low.endswith("db"):
        db = units.ratio_db(text)
        lines = [f"{db:g} dB = {core.db_to_linear(db):.4g}x power  ({10 ** (db / 20):.4g}x amplitude)"]
    else:
        db = units.ratio_db(text)
        lines = [f"{text}x power = {db:.2f} dB"]
    say(lines, a.quiet)


# ---------------------------------------------------------------- parser
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="shannon-says", description="Tiny comms-engineering calculator.")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("-q", "--quiet", action="store_true", help="numbers only, no commentary")
    sub = p.add_subparsers(dest="cmd", metavar="COMMAND")

    c = sub.add_parser("capacity", help="Shannon-Hartley capacity  (C = B log2(1+SNR))")
    c.add_argument("--bw", dest="bandwidth", required=True, help="bandwidth, e.g. 20MHz")
    c.add_argument("--snr", required=True, help="SNR, e.g. 15dB or a linear ratio like 31")
    c.set_defaults(func=cmd_capacity)

    n = sub.add_parser("need", help="minimum SNR to reach a target data rate")
    n.add_argument("--bw", dest="bandwidth", required=True, help="bandwidth, e.g. 20MHz")
    n.add_argument("--rate", required=True, help="target rate in bit/s with SI prefix, e.g. 100M")
    n.set_defaults(func=cmd_need)

    d = sub.add_parser("db", help="convert dB / dBm / dBW / W / linear ratios")
    d.add_argument("value", help="e.g. 3dB, 30dBm, 0dBW, 100mW, 2")
    d.set_defaults(func=cmd_db)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 0
    try:
        args.func(args)
    except (UnitError, ValueError) as e:
        print(f"shannon-says: {e}", file=sys.stderr)
        return 2
    return 0
