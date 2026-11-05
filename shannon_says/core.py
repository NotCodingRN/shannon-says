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


SPEED_OF_LIGHT = 299_792_458.0
THERMAL_NOISE_DBM_PER_HZ = -174.0  # kT at 290 K


def wavelength(freq_hz: float) -> float:
    return SPEED_OF_LIGHT / freq_hz


def fspl_db(distance_m: float, freq_hz: float) -> float:
    """Free-space path loss: 20*log10(4*pi*d*f/c)."""
    if distance_m <= 0 or freq_hz <= 0:
        raise ValueError("distance and frequency must be > 0")
    return 20 * math.log10(4 * math.pi * distance_m * freq_hz / SPEED_OF_LIGHT)


def noise_floor_dbm(bandwidth_hz: float, noise_figure_db: float = 0.0) -> float:
    """Thermal noise power in the receiver bandwidth: -174 dBm/Hz + 10*log10(B) + NF."""
    return THERMAL_NOISE_DBM_PER_HZ + 10 * math.log10(bandwidth_hz) + noise_figure_db


def link_budget(tx_dbm: float, freq_hz: float, distance_m: float, bandwidth_hz: float,
                tx_gain_db: float = 0.0, rx_gain_db: float = 0.0, losses_db: float = 0.0,
                noise_figure_db: float = 0.0) -> dict:
    """Received power, SNR and resulting Shannon capacity for a free-space link."""
    loss = fspl_db(distance_m, freq_hz)
    rx = tx_dbm + tx_gain_db + rx_gain_db - loss - losses_db
    noise = noise_floor_dbm(bandwidth_hz, noise_figure_db)
    snr = rx - noise
    return {"fspl_db": loss, "rx_dbm": rx, "noise_dbm": noise, "snr_db": snr,
            "capacity_bps": capacity(bandwidth_hz, snr)}


def snr_needed(bandwidth_hz: float, rate_bps: float) -> float:
    """Minimum SNR (dB) to carry rate_bps over bandwidth_hz: SNR = 2^(R/B) - 1."""
    if bandwidth_hz <= 0 or rate_bps <= 0:
        raise ValueError("bandwidth and rate must be > 0")
    return linear_to_db(2 ** (rate_bps / bandwidth_hz) - 1)
