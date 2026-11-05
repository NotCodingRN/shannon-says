# shannon-says 📡

[![tests](https://github.com/NotCodingRN/shannon-says/actions/workflows/tests.yml/badge.svg)](https://github.com/NotCodingRN/shannon-says/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)
![dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)
![license](https://img.shields.io/badge/license-MIT-blue)

> *Information is surprise. This calculator tries very hard not to be.*

A tiny command-line calculator for communications engineering: the stuff you redo on paper every lab.

## What it does

**Channel capacity** (Shannon–Hartley, `C = B·log2(1 + SNR)`):

```console
$ shannon-says capacity --bw 20MHz --snr 15dB
Bandwidth            20 MHz
SNR                  15.00 dB  (31.62x)
Capacity             101 Mbit/s
Spectral efficiency  5.028 bit/s/Hz
Shannon says: Noise always gets a vote.
```

**How much SNR do I need** for a target rate?

```console
$ shannon-says need --bw 20MHz --rate 100M
To push 100 Mbit/s through 20 MHz
you need at least    14.91 dB SNR  (31x)
```

**dB conversions** (dB, dBm, dBW, W, mW, linear):

```console
$ shannon-says db 30dBm
30 dBm = 1 W = 0 dBW
$ shannon-says db 100mW
100mW = 20.00 dBm = -10.00 dBW
$ shannon-says db 3dB
3 dB = 1.995x power  (1.413x amplitude)
```

**Free-space path loss**:

```console
$ shannon-says fspl --freq 2.4GHz --distance 100m
Frequency            2.4 GHz  (wavelength 12.5 cm)
Distance             100 m
Free-space loss      80.05 dB
```

**Full link budget**: TX power, antennas, path loss, noise floor, SNR, capacity and margin in one go:

```console
$ shannon-says link --tx 20dBm --freq 2.4GHz --distance 100m --bw 20MHz \
                    --gtx 2dB --grx 2dB --nf 6dB --required 25dB
Free-space loss      80.05 dB
Received power       -56.05 dBm
Noise floor          -94.99 dBm
SNR                  38.94 dB
Shannon capacity     259 Mbit/s
Link margin          +13.94 dB  (closes)
```

Add `-q` before the command to drop the commentary.

## Install

```bash
git clone https://github.com/NotCodingRN/shannon-says
cd shannon-says
pip install .
shannon-says --help
```

No dependencies, just Python 3.9+.

## Tests

```bash
python -m unittest discover -s tests -v
```

Reference checks include the 1 MHz / SNR 31 → 5 Mbit/s textbook case, FSPL at 1 GHz / 1 km = 92.45 dB, and the −1.59 dB Shannon limit.

## License

MIT
