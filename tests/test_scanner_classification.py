import unittest
from unittest.mock import patch, MagicMock
import socket
from netguard.scanner import scan_port, PortState
from netguard.service import lookup_service

class TestScannerClassification(unittest.TestCase):
    def setUp(self):
        # Patch the service lookup to a deterministic value
        self.patcher_lookup = patch('netguard.scanner.lookup_service', return_value='http')
        self.mock_lookup = self.patcher_lookup.start()
        self.addCleanup(self.patcher_lookup.stop)

    def _mock_socket(self, connect_side_effect=None):
        mock_sock = MagicMock()
        mock_sock.settimeout.return_value = None
        mock_sock.close.return_value = None
        if connect_side_effect is not None:
            mock_sock.connect.side_effect = connect_side_effect
        else:
            mock_sock.connect.return_value = None
        return mock_sock

    @patch('netguard.scanner.socket')
    def test_open_port(self, mock_socket_module):
        mock_socket_module.AF_INET = socket.AF_INET
        mock_socket_module.SOCK_STREAM = socket.SOCK_STREAM
        mock_socket_module.socket.return_value = self._mock_socket()
        result = scan_port('127.0.0.1', 80, timeout=1.0)
        self.assertEqual(result.state, PortState.OPEN)
        self.assertEqual(result.service, 'http')
        self.assertIsNotNone(result.elapsed)

    @patch('netguard.scanner.socket')
    def test_closed_port(self, mock_socket_module):
        mock_socket_module.AF_INET = socket.AF_INET
        mock_socket_module.SOCK_STREAM = socket.SOCK_STREAM
        mock_socket_module.socket.return_value = self._mock_socket(connect_side_effect=ConnectionRefusedError())
        result = scan_port('127.0.0.1', 22, timeout=1.0)
        self.assertEqual(result.state, PortState.CLOSED)
        self.assertEqual(result.service, 'UNKNOWN')
        self.assertIsNone(result.elapsed)

    @patch('netguard.scanner.socket')
    def test_timeout_port(self, mock_socket_module):
        mock_socket_module.AF_INET = socket.AF_INET
        mock_socket_module.SOCK_STREAM = socket.SOCK_STREAM
        mock_socket_module.socket.return_value = self._mock_socket(connect_side_effect=socket.timeout())
        result = scan_port('127.0.0.1', 23, timeout=0.5)
        self.assertEqual(result.state, PortState.TIMEOUT)
        self.assertEqual(result.service, 'UNKNOWN')
        self.assertIsNone(result.elapsed)

    @patch('netguard.scanner.socket')
    def test_error_port(self, mock_socket_module):
        mock_socket_module.AF_INET = socket.AF_INET
        mock_socket_module.SOCK_STREAM = socket.SOCK_STREAM
        mock_socket_module.socket.return_value = self._mock_socket(connect_side_effect=OSError('boom'))
        result = scan_port('127.0.0.1', 24, timeout=1.0)
        self.assertEqual(result.state, PortState.ERROR)
        self.assertEqual(result.service, 'UNKNOWN')
        self.assertIsNone(result.elapsed)

if __name__ == '__main__':
    unittest.main()
