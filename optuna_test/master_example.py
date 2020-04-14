import uuid
import json
import optuna
import socket
from concurrent.futures import ThreadPoolExecutor

# number of parallel trials
NUM_PAR = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('localhost', 10000)
sock.bind(server_address)
sock.listen(NUM_PAR)


def objective(trial):
    con, addr = sock.accept()
    x = trial.suggest_uniform('x', -10, 10)
    con.sendall(json.dumps(x).encode())
    d = con.recv(1024)
    con.close()
    return json.loads(d)


db_name = 'sqlite:///test.db'
study_name=str(uuid.uuid4())


def func():
    study = optuna.load_study(study_name=study_name, storage=db_name)
    study.optimize(objective, n_trials=10 // NUM_PAR)


study = optuna.create_study(study_name=study_name, storage=db_name)


with ThreadPoolExecutor(max_workers=NUM_PAR) as ex:
    for i in range(NUM_PAR):
        ex.submit(func)

study = optuna.load_study(study_name=study_name, storage=db_name)
print(study.best_params)