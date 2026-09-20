import subprocess
import sys
import os
import unittest

SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'netguard.py'))

class TestCLIInvalidInputs(unittest.TestCase):
    def run_cmd(self, args):
        cmd = [sys.executable, SCRIPT_PATH] + args
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result

    def test_invalid_port(self):
        res = self.run_cmd(['-t', '127.0.0.1', '-p', '0'])
        self.assertNotEqual(res.returncode, 0)

    def test_invalid_port_range(self):
        res = self.run_cmd(['-t', '127.0.0.1', '-p', '100-50'])
        self.assertNotEqual(res.returncode, 0)

    def test_invalid_timeout(self):
        res = self.run_cmd(['-t', '127.0.0.1', '-p', '22', '--timeout', '-1'])
        self.assertNotEqual(res.returncode, 0)

    def test_invalid_workers(self):
        res = self.run_cmd(['-t', '127.0.0.1', '-p', '22', '--workers', '0'])
        self.assertNotEqual(res.returncode, 0)

    def test_invalid_target(self):
        res = self.run_cmd(['-t', 'not_an_ip', '-p', '22'])
        self.assertNotEqual(res.returncode, 0)

if __name__ == '__main__':
    unittest.main()
