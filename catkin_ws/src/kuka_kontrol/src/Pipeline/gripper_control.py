import socket
import time


class GripperControl:
    host: str
    port: int
    lsock: socket.socket

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.lsock.connect((self.host, self.port))

    def listen(self):
        return self.lsock.recv(1024)

    def command_calibration(self):
        self.lsock.send(b"command_calibration")

    def command_close(self):
        self.lsock.send(b"command_close")

    def command_open(self):
        self.lsock.send(b"command_open")


if __name__ == "__main__":
    control = GripperControl("172.31.1.171", 5500)
    control.connect()
    control.command_calibration()
    control.listen()
    control.command_close()
    control.listen()
    control.command_open()
    control.listen()

