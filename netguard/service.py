import socket

def lookup_service(port: int) -> str:
    """Return a common service name for *port* using the OS service database.

    If the service cannot be resolved, returns the string "UNKNOWN".
    """
    try:
        return socket.getservbyport(port)
    except OSError:
        return "UNKNOWN"
