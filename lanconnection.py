import json
import socket


class LanConnection:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        print(self.sock.recv(1024).decode('utf8'))

    def do_cmd(self, obj):
        self.sock.sendall((json.dumps(obj)).encode("utf8"))
        res = self.sock.recv(1024)
        if res:
            res = json.loads(res)
            return res

    def close_connection(self):
        self.sock.sendall((json.dumps(['!disconnect']).encode("utf8")))
