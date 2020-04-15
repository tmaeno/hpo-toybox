import nevergrad as ng

from evaluation import evaluation

inst = ng.p.Instrumentation(ng.p.Array(shape=(2,)), y=ng.p.Scalar())
optimizer = ng.optimizers.OnePlusOne(parametrization=inst, budget=100)

for _ in range(optimizer.budget):
    x = optimizer.ask()
    loss = evaluation(*x.args, **x.kwargs)
    optimizer.tell(x, loss)

recommendation = optimizer.provide_recommendation()
print(recommendation.value)
