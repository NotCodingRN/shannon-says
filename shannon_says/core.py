"""The actual math. Pure functions, SI units in, SI units out."""
from __future__ import annotations

import math

SHANNON_LIMIT_EBN0_DB = 10 * math.log10(math.log(2))  # -1.59 dB


def db_to_linear(db: float) -> float:
    return 10 ** (db / 10)


def linear_to_db(ratio: float) -> float:
    if ratio <= 0:
        raise ValueError("ratio must be > 0")
    return 10 * math.log10(ratio)


def dbm_to_watts(dbm: float) -> float:
    return 10 ** ((dbm - 30) / 10)


def watts_to_dbm(watts: float) -> float:
    if watts <= 0:
        raise ValueError("power must be > 0")
    return 10 * math.log10(watts) + 30


def capacity(bandwidth_hz: float, snr_db: float) -> float:
    """Shannon-Hartley: C = B * log2(1 + SNR), in bit/s."""
    if bandwidth_hz <= 0:
        raise ValueError("bandwidth must be > 0")
    return bandwidth_hz * math.log2(1 + db_to_linear(snr_db))


def spectral_efficiency(snr_db: float) -> float:
    """bit/s/Hz at the Shannon limit."""
    return math.log2(1 + db_to_linear(snr_db))


def snr_needed(bandwidth_hz: float, rate_bps: float) -> float:
    """Minimum SNR (dB) to carry rate_bps over bandwidth_hz: SNR = 2^(R/B) - 1."""
    if bandwidth_hz <= 0 or rate_bps <= 0:
        raise ValueError("bandwidth and rate must be > 0")
    return linear_to_db(2 ** (rate_bps / bandwidth_hz) - 1)
