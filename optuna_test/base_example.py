import optuna

from objective_body import objective_body


def objective(trial):
    x = trial.suggest_uniform('x', -10, 10)
    return objective_body(x)


study = optuna.create_study()
study.optimize(objective, n_trials=10)
print(study.best_params)