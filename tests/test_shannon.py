import io
import unittest
from contextlib import redirect_stdout

from shannon_says import cli, core, units


class TestUnits(unittest.TestCase):
    def test_frequency(self):
        self.assertEqual(units.frequency("2.4GHz"), 2.4e9)
        self.assertEqual(units.frequency("20 MHz"), 20e6)
        self.assertEqual(units.frequency("1000"), 1000)

    def test_rate(self):
        self.assertEqual(units.rate("100M"), 100e6)
        self.assertEqual(units.rate("1.5Gbit/s"), 1.5e9)
        self.assertEqual(units.rate("64kbps"), 64e3)

    def test_power(self):
        self.assertAlmostEqual(units.power_dbm("1W"), 30)
        self.assertAlmostEqual(units.power_dbm("100mW"), 20)
        self.assertAlmostEqual(units.power_dbm("0dBW"), 30)

    def test_ratio(self):
        self.assertEqual(units.ratio_db("15dB"), 15)
        self.assertAlmostEqual(units.ratio_db("100"), 20)

    def test_bad_input(self):
        with self.assertRaises(units.UnitError):
            units.frequency("5parsecs")
        with self.assertRaises(units.UnitError):
            units.ratio_db("-3")


class TestCore(unittest.TestCase):
    def test_textbook_capacity(self):
        # 1 MHz at linear SNR 31 -> log2(32) = 5 bit/s/Hz -> 5 Mbit/s
        self.assertAlmostEqual(core.capacity(1e6, core.linear_to_db(31)), 5e6, places=3)

    def test_snr_needed_inverts_capacity(self):
        snr = core.snr_needed(20e6, 100e6)
        self.assertAlmostEqual(core.capacity(20e6, snr), 100e6, places=2)

    def test_fspl_reference_values(self):
        self.assertAlmostEqual(core.fspl_db(1000, 1e9), 92.45, places=2)
        self.assertAlmostEqual(core.fspl_db(100, 2.4e9), 80.05, places=2)

    def test_noise_floor(self):
        self.assertAlmostEqual(core.noise_floor_dbm(1), -174.0)
        self.assertAlmostEqual(core.noise_floor_dbm(20e6, 6), -94.99, places=2)

    def test_dbm_watts_roundtrip(self):
        self.assertAlmostEqual(core.watts_to_dbm(core.dbm_to_watts(17.3)), 17.3)

    def test_shannon_limit(self):
        self.assertAlmostEqual(core.SHANNON_LIMIT_EBN0_DB, -1.59, places=2)


class TestCli(unittest.TestCase):
    def run_cli(self, *args):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = cli.main(["-q", *args])
        return code, buf.getvalue()

    def test_capacity_command(self):
        code, out = self.run_cli("capacity", "--bw", "1MHz", "--snr", "31")
        self.assertEqual(code, 0)
        self.assertIn("5 Mbit/s", out)

    def test_link_margin(self):
        code, out = self.run_cli("link", "--tx", "20dBm", "--freq", "2.4GHz", "--distance", "100m",
                                 "--bw", "20MHz", "--nf", "6dB", "--required", "25dB")
        self.assertEqual(code, 0)
        self.assertIn("closes", out)

    def test_bad_unit_exit_code(self):
        self.assertEqual(cli.main(["db", "5xyz"]), 2)


if __name__ == "__main__":
    unittest.main()
