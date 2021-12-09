import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, transpile, assemble
import math
import random
import numpy as np
from scipy.optimize import minimize
from circuit import had_test_circuit_short, had_test_circuit_long, specialh_circuit_short_I, specialh_circuit_long_I, specialh_circuit_short_Z3, specialh_circuit_long_Z3

# A = 0.45Z_3 + 0.55I
coefficient_set = [0.55, 0.45]
gate_set = [[0, 0, 0], [0, 0, 1]]

def had_test(parameters):
    #이곳에 가져온 had_test를 넣어주면 된다
    return had_test_circuit_short(parameters)

def specialh_I(parameters):
    return specialh_circuit_short_I(parameters)

def specialh_Z3(parameters):
    return specialh_circuit_short_Z3(parameters)

# ========================= learning start =========================
# A = 0.55I + 0.225Z_2 + 0.225Z_3
# Implements the entire cost function on the quantum circuit

def calculate_cost_function(parameters, op_obj, callback):
    
    global opt

    overall_sum_1 = 0
    
    parameters = [parameters[0:3], parameters[3:6], parameters[6:9]]

    for i in range(0, len(gate_set)):
        for j in range(0, len(gate_set)):

            global circ
            
            multiply = coefficient_set[i]*coefficient_set[j]
            if(i != j):
                m_sum = had_test(parameters) # i != j 이면 CZ_3 가 있는 회로, 이게 우리가 구현했던 had_test_circuit_short 임
            else :
                m_sum = 0 # 임시로 이렇게 구현, i=j 이면 A^* A = I 여서 아무런 효과 없는 것과 마찬가지. (A = 0.55I + 0.45Z3 문제에 한정적)

            overall_sum_1+=multiply*(1-(2*m_sum))

    overall_sum_2 = 0

    for i in range(0, len(gate_set)):
        for j in range(0, len(gate_set)):

            multiply = coefficient_set[i]*coefficient_set[j]
            mult = 1

            for extra in range(0, 2):
                
                if (extra == 0):
                    #special_had_test(gate_set[i], [1, 2, 3], 0, parameters, qctl)
                    if (gate_set[i]==[0,0,0]):
                        m_sum = specialh_I(parameters)
                    elif (gate_set[i]==[0,0,1]):
                        m_sum = specialh_Z3(parameters)

                if (extra == 1):
                    #special_had_test(gate_set[j], [1, 2, 3], 0, parameters, qctl)
                    if (gate_set[j]==[0,0,0]):
                        m_sum = specialh_I(parameters)
                    elif (gate_set[j]==[0,0,1]):
                        m_sum = specialh_Z3(parameters)
                
                m_sum = 1-m_sum #이건 실수, mathematica 파일 바꿔야함 

                mult = mult*(1-(2*m_sum))

            overall_sum_2+=multiply*mult
            
    print(1-float(overall_sum_2/overall_sum_1))
    callback(xk= 1-float(overall_sum_2/overall_sum_1), obj=op_obj)

    return 1-float(overall_sum_2/overall_sum_1)

