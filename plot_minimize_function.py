import matplotlib.pyplot as plt
import scipy.optimize as op
import numpy as np
from functools import partial

Q = np.array([[1.0, 0.75, 0.45], [0.75, 1.0, 0.60], [0.45, 0.60, 1.0]])
a = 1.0

def _fun(x, Q, a):
    c = np.einsum('i,ij,j->', x, Q, x)
    p = np.sum(a * np.abs(x))
    return c + p
def _constr(x):
    return np.sum(x) - 1

class OpObj(object):
    def __init__(self, Q, a):
        self.Q, self.a = Q, a
        rv = np.random.rand()
        self.x_0 = np.array([rv, (1-rv)/2, (1-rv)/2])
        self.f = np.full(shape=(500,), fill_value=np.NaN)
        self.count = 0
    def _fun(self, x):
        return _fun(x, self.Q, self.a)

def cb(xk, obj=None):
    obj.f[obj.count] = obj._fun(xk)
    obj.count += 1

fig, ax = plt.subplots(1,1)
x = np.linspace(1,500,500)
for test in range(20):
    op_obj = OpObj(Q, a)
    x_soln = op.minimize(_fun, op_obj.x_0, args=(Q, a), method='SLSQP',
                         constraints={'type': 'eq', 'fun': _constr},
                         callback=partial(cb, obj=op_obj))
    ax.plot(x, op_obj.f)

ax.set_ylim((0,1))
plt.show()