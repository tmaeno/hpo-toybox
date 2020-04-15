import sys
import socket
import pickle
from evaluation import evaluation

server_address = ('localhost', 10000)

nn = int(sys.argv[1])
for _ in range(nn):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(server_address)
        sock.sendall(pickle.dumps({'command': 'ask'}))
        x = pickle.loads(sock.recv(16384))
        if x == 'end':
            print ("No more ask")
            break
        loss = evaluation(*x.args, **x.kwargs)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(server_address)
        sock.sendall(pickle.dumps({'command': 'tell', 'sample': x, 'loss': loss}))
