import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
import time

n = 600
scores = np.random.rand(n)
costs = np.random.rand(n) * 1000
budget = 150000
n_select = 40

start = time.time()
c = -scores
A = np.vstack([costs, np.ones(n)])
b_l = np.array([-np.inf, n_select])
b_u = np.array([budget, n_select])

constraints = LinearConstraint(A, b_l, b_u)
integrality = np.ones(n, dtype=int)
bounds = Bounds(0, 1)

res = milp(c=c, constraints=constraints, integrality=integrality, bounds=bounds)

print("Time:", time.time() - start)
print("Status:", res.status)
print("Message:", res.message)
if res.success:
    selected = np.round(res.x).astype(int)
    print("Selected:", selected.sum())
    print("Cost:", np.dot(costs, selected))
    print("Score:", np.dot(scores, selected))
