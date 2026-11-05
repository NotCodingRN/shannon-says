# shannon-says 📡

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

Add `-q` before the command to drop the commentary.

## Install

```bash
git clone https://github.com/NotCodingRN/shannon-says
cd shannon-says
pip install .
shannon-says --help
```

No dependencies, just Python 3.9+.

## License

MIT
