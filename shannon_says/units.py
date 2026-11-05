"""Parse human-friendly quantities like "20MHz", "15dB", "30dBm", "2.4GHz", "5km"."""
from __future__ import annotations

import math
import re

_NUM = r"([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)"

FREQ = {"hz": 1.0, "khz": 1e3, "mhz": 1e6, "ghz": 1e9, "thz": 1e12}
DIST = {"mm": 1e-3, "cm": 1e-2, "m": 1.0, "km": 1e3, "mi": 1609.344}


class UnitError(ValueError):
    pass


def _split(text: str) -> tuple[float, str]:
    m = re.fullmatch(_NUM + r"\s*([a-zA-Z/]*)", text.strip())
    if not m:
        raise UnitError(f"can't read {text!r} (try something like 20MHz, 15dB, 30dBm)")
    return float(m.group(1)), m.group(2).lower()


def frequency(text: str) -> float:
    """'2.4GHz' -> 2.4e9 (Hz). A bare number is taken as Hz."""
    value, unit = _split(text)
    unit = unit or "hz"
    if unit not in FREQ:
        raise UnitError(f"unknown frequency unit {unit!r} (use Hz, kHz, MHz, GHz)")
    return value * FREQ[unit]


def distance(text: str) -> float:
    """'5km' -> 5000 (m). A bare number is taken as metres."""
    value, unit = _split(text)
    unit = unit or "m"
    if unit not in DIST:
        raise UnitError(f"unknown distance unit {unit!r} (use m, km, mi)")
    return value * DIST[unit]


def ratio_db(text: str) -> float:
    """'15dB' -> 15. A bare number is treated as a LINEAR ratio and converted to dB."""
    value, unit = _split(text)
    if unit == "db":
        return value
    if unit == "":
        if value <= 0:
            raise UnitError("a linear ratio must be > 0")
        return 10 * math.log10(value)
    raise UnitError(f"unknown ratio unit {unit!r} (use dB, or a plain linear number)")


def power_dbm(text: str) -> float:
    """'30dBm' -> 30, '1W' -> 30, '100mW' -> 20, '0dBW' -> 30."""
    value, unit = _split(text)
    if unit == "dbm":
        return value
    if unit == "dbw":
        return value + 30
    scale = {"w": 1.0, "mw": 1e-3, "uw": 1e-6, "kw": 1e3}.get(unit)
    if scale is None:
        raise UnitError(f"unknown power unit {unit!r} (use dBm, dBW, W, mW)")
    if value <= 0:
        raise UnitError("power in watts must be > 0")
    return 10 * math.log10(value * scale * 1e3)


def pretty_rate(bits_per_s: float) -> str:
    for unit, scale in (("Tbit/s", 1e12), ("Gbit/s", 1e9), ("Mbit/s", 1e6), ("kbit/s", 1e3)):
        if bits_per_s >= scale:
            return f"{bits_per_s / scale:.3g} {unit}"
    return f"{bits_per_s:.3g} bit/s"


def pretty_freq(hz: float) -> str:
    for unit, scale in (("GHz", 1e9), ("MHz", 1e6), ("kHz", 1e3)):
        if hz >= scale:
            return f"{hz / scale:g} {unit}"
    return f"{hz:g} Hz"
