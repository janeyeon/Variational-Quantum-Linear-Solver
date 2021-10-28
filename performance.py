import qiskit
from qiskit import QuantumCircuit
from qiskit import Aer, execute
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import dataExtraction as de
import simulator as sim
from scipy.optimize import minimize

"""==========Input Data Sets Here and Polynomial Order================"""

x = np.arange(0,32,1)
y = (2*x-1)**3 + [random.uniform(-1,1) for p in range(32)]
print("y: ", y)

order = 3

"""=======================Necessary Functions========================="""

#Code for computing inner products on a real quantum computer
def inner_prod(vec1, vec2):
    # 32x1, 32x1 짜리 vector 2개 
    #first check lengths are equal
    if len(vec1) != len(vec2):
        raise ValueError('Lengths of states are not equal')
    
    # 여기에서 circuit 부분을 우리가 만든 함수로 대체한다 
    # 다만... circuit 이 바뀜으로 inner prod 부분이 달라져야 할듯함
    circ = QuantumCircuit(nqubits+1,1)
    # vec : 64x1 짜리 vector 
    vec = np.concatenate((vec1,vec2))/np.sqrt(2)
    
    
    # circ.initialize(vec, range(nqubits+1))
    # circ.h(nqubits)
    # circ.measure(nqubits,0)

    # print(circ.draw())

    # backend = Aer.get_backend('qasm_simulator')
    # job = execute(circ, backend, shots=10000)

    # result = job.result()
    # print("result: ", result)
    # outputstate = result.get_counts(circ)
    # print("outputState: ", outputstate)

    # if ('0' in outputstate.keys()):
    #     m_sum = float(outputstate["0"])/10000
    # else:
    #     m_sum = 0
     
    # #1x4 
    # print("m_sum: ", 2*m_sum-1)

    #여기에서 부터 내 코드를 사용하면 됨 
    qc = sim.quantum_computer(nqubits + 1)

    qc.h(nqubits)
    
    return 2*m_sum-1

#Returns the cost functions, based on n parameters for an n-th order polynomial
def calculate_cost_function_n(parameters):
    print("parameters: ", type(parameters))
    yphi = parameters[0]*np.sqrt(N)/ynorm*inner_prods[0]

    for i in range(1,len(parameters)):

        xpow = x**i
        xnormpow = np.linalg.norm(xpow)
        xpow = xpow/xnormpow
        
        yphi += parameters[i]*xnormpow/ynorm*inner_prods[i]
    
    print((1-yphi)**2)
    return (1-yphi)**2

def return_fits(xfit):
    c_fit = np.zeros(100)
    q_fit = np.zeros(100)
    for i in range(order+1):
        q_fit += xfit**i*out['x'][i]
        c_fit += xfit**i*class_fit[i]

    return q_fit, c_fit

"""===============Normalising y data set and \ket{1}====================="""

N = len(x)
nqubits = math.ceil(np.log2(N))
ones = np.ones(N)/np.sqrt(N)

ynorm = np.linalg.norm(y)
y = y/ynorm

"""===========Computing inner products once off to save time============="""

inner_prods = np.zeros(order+1)
inner_prods[0] = inner_prod(y,ones)

for i in range(1,order+1):

    xpow = x**i
    xnormpow = np.linalg.norm(xpow)
    xpow = xpow/xnormpow
    
    inner_prods[i] = inner_prod(y,xpow)
    
"""=================Running Classical Optimiser========================="""
print("inner prods: ", inner_prods)
#Random initial guess for parameters
x0 = [random.uniform(-10,10) for p in range(order+1)]
#Can change the optimiser method here
#구한 cost function 의 공식에서 minimize 할 수 있는 out 을 만드는듯 
#
print("function", calculate_cost_function_n)
print("function type", type(calculate_cost_function_n))
out = minimize(calculate_cost_function_n, x0=x0, method="BFGS", options={'maxiter':200}, tol=1e-6)
#Classical fit
class_fit = np.polyfit(x,y*ynorm,order)
class_fit = class_fit[::-1]

print("Variational Quantum Fit: ", out['x'])
print("Classical Fit: ", class_fit)

"""==========================Plotting===================================="""

xfit = np.linspace(min(x), max(x), 100)
q_fit, c_fit = return_fits(xfit)

plt.scatter(x,y*ynorm)
plt.plot(xfit, q_fit, label='Quantum')
plt.plot(xfit, c_fit, label='Classical')
plt.legend()
plt.title("Fitting to $y = (2x-1)^3$ + rand(-1,1)")
plt.xlabel("x")
plt.ylabel("y")
plt.show()