import nevergrad as ng
import pickle
import socket

opt_filename = '/tmp/optimizer.pkl'

inst = ng.p.Instrumentation(ng.p.Array(shape=(2,)), y=ng.p.Scalar())
optimizer = ng.optimizers.OnePlusOne(parametrization=inst, budget=100)
optimizer.dump(opt_filename)

# number of parallel trials
NUM_PAR = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('localhost', 10000)
sock.bind(server_address)
sock.listen(NUM_PAR)

while True:
    to_terminated = False
    con, addr = sock.accept()
    m = pickle.loads(con.recv(16384))
    optimizer = ng.optimizers.OnePlusOne.load(opt_filename)
    if m['command'] == 'ask':
        if optimizer.num_ask >= optimizer.budget:
            x = 'end'
        else:
            x = optimizer.ask()
    else:
        x = None
        optimizer.tell(m['sample'], m['loss'])
        if optimizer.num_tell - optimizer.num_tell_not_asked >= optimizer.budget:
            to_terminated = True
    if x is not None:
        con.sendall(pickle.dumps(x))
    con.close()
    optimizer.dump(opt_filename)
    if to_terminated:
        break

optimizer = ng.optimizers.OnePlusOne.load(opt_filename)
recommendation = optimizer.provide_recommendation()
print(recommendation.value)
