import socket

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 5000))
    s.listen(5)

    (conn, address) = s.accept()
    while True:
        # accept connections from outside
        print("recv: ", conn.recv(1024))

