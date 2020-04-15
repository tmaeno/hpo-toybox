import socket
import json
from evaluation import evaluation

server_address = ('localhost', 10000)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(server_address)
    x = sock.recv(1024)
    x = json.loads(x)
    d = evaluation(x)
    sock.sendall(json.dumps(d).encode())