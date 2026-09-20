import unittest
from netguard.service import lookup_service

class TestServiceLookup(unittest.TestCase):
    def test_known_service(self):
        # Port 80 is typically http
        self.assertEqual(lookup_service(80).lower(), "http")

    def test_unknown_service(self):
        # Choose a high port unlikely to be registered
        self.assertEqual(lookup_service(65000), "UNKNOWN")

if __name__ == "__main__":
    unittest.main()
