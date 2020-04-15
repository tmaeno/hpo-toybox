import optuna
from optuna.pruners import SuccessiveHalvingPruner

from evaluation import evaluation


def objective(trial):
    x = trial.suggest_uniform('x', -10, 10)
    return evaluation(x)


study = optuna.create_study(pruner=SuccessiveHalvingPruner())
study.optimize(objective, n_trials=10)
print(study.best_params)