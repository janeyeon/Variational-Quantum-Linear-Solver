import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, transpile, assemble
import math
import random
import numpy as np
from scipy.optimize import minimize
from circuit import had_test_circuit_long, had_test_circuit_short, specialh_circuit_short, specialh_circuit_long

coefficient_set = [0.55, 0.45]
gate_set = [[0, 0, 0], [0, 0, 1]]

class customVQLS:
    def __init__(self, is_short = false):
        self.is_short = is_short

    # Creates the Hadamard test

    def had_test(self, parameters):
        if self.is_short:
             #이곳에 가져온 had_test를 넣어주면 된다
            return had_test_circuit_short(parameters).evalf()
        else:
            return had_test_circuit_long(parameters).evalf()

    # Create the controlled Hadamard test, for calculating <psi|psi>

    def special_had_test(self, gate_type, qubits, auxiliary_index, parameters, reg):
        if self.is_short:
            return specialh_circuit_short(parameters).evalf()
        else: 
            return specialh_circuit_long(parameters).evalf()


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
                    m_sum = had_test(parameters)
                else :
                    m_sum = 0 # 임시로 이렇게 구현

                overall_sum_1+=multiply*(1-(2*m_sum))

        overall_sum_2 = 0

        for i in range(0, len(gate_set)):
            for j in range(0, len(gate_set)):

                multiply = coefficient_set[i]*coefficient_set[j]
                mult = 1

                for extra in range(0, 2):

                    qctl = QuantumRegister(5)
                    qc = ClassicalRegister(5)
                    circ = QuantumCircuit(qctl, qc)

                    backend = Aer.get_backend('aer_simulator')

                    if (extra == 0):
                        special_had_test(gate_set[i], [1, 2, 3], 0, parameters, qctl)
                    if (extra == 1):
                        special_had_test(gate_set[j], [1, 2, 3], 0, parameters, qctl)

                    circ.save_statevector()    
                    t_circ = transpile(circ, backend)
                    qobj = assemble(t_circ)
                    job = backend.run(qobj)

                    result = job.result()
                    outputstate = np.real(result.get_statevector(circ, decimals=100))
                    o = outputstate

                    m_sum = 0
                    for l in range (0, len(o)):
                        if (l%2 == 1):
                            n = o[l]**2
                            m_sum+=n
                    mult = mult*(1-(2*m_sum))

                overall_sum_2+=multiply*mult
                
        print(1-float(overall_sum_2/overall_sum_1))
        callback(xk= 1-float(overall_sum_2/overall_sum_1), obj=op_obj)

        return 1-float(overall_sum_2/overall_sum_1)

