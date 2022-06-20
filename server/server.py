import socket


class Server:
    def __init__(self, addr, port, conn_count=5):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((addr, port))
        self.__server.listen(conn_count)

    def send_msg(self, msg):
        conn, _ = self.__server.accept()
        conn.send(msg)
        conn.close()

    def recv_msg(self, size=1024):
        conn, _ = self.__server.accept()
        msg = conn.recv(size)
        conn.close()
        return msg


if __name__ == '__main__':
    server = Server('localhost', 23333)
    while True:
        print(server.recv_msg().decode())
