import unittest
from netguard.utils import parse_ports

class TestPortParsing(unittest.TestCase):
    def test_single_port(self):
        self.assertEqual(parse_ports("80"), [80])

    def test_multiple_ports(self):
        self.assertEqual(parse_ports("22,80,443"), [22, 80, 443])

    def test_range(self):
        self.assertEqual(parse_ports("1-3"), [1, 2, 3])

    def test_combined(self):
        self.assertEqual(parse_ports("22,80-82,443"), [22, 80, 81, 82, 443])

    def test_invalid_port(self):
        with self.assertRaises(ValueError):
            parse_ports("0")
        with self.assertRaises(ValueError):
            parse_ports("70000")

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            parse_ports("10-5")
        with self.assertRaises(ValueError):
            parse_ports("a-b")

if __name__ == "__main__":
    unittest.main()
