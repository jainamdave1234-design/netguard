import socket
import time

ports = [22, 80, 135, 443, 445]

for port in ports:

    s = socket.socket()
    s.settimeout(1)

    try:
        start = time.time()

        s.connect(("127.0.0.1", port))

        end = time.time()

        try:
            service = socket.getservbyport(port)
        except:
            service = "Unknown"
        print("Port", port, "is OPEN — Service:", service)

    except:
        print("Port", port, "is CLOSED")

    s.close()