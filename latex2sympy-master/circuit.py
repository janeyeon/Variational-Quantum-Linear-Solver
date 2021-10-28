import sympy 
import numpy as np
from sympy.core.symbol import symbols
from process_latex import process_sympy
from dataExtraction import h_test_short_ex, h_test_long_ex, specialh_long_ex, specialh_short_ex

def had_test_circuit_short(parameters): 
    # 그리고 대입 
    result = h_test_short_sym_ex.subs({a : parameters[0][0], b : parameters[0][1], c : parameters[0][2], d : parameters[1][0], e : parameters[1][1], f : parameters[1][2], g : parameters[2][0], h : parameters[2][1], j : parameters[2][2]})

    # result = h_test_short_sym_ex.subs({a : parameters[0][0], b : parameters[1][0], c : parameters[2][0], d : parameters[0][1], e : parameters[1][1], f : parameters[2][1], g : parameters[0][2], h : parameters[1][2], i : parameters[2][2]})

    return result 

def had_test_circuit_long(parameters): 
    # 그리고 대입 
    result2 = h_test_long_sym_ex.subs({a : parameters[0][0], b : parameters[0][1], c : parameters[0][2], d : parameters[1][0], e : parameters[1][1], f : parameters[1][2], g : parameters[2][0], h : parameters[2][1], j : parameters[2][2]})
    return result2

def specialh_circuit_short(parameters): 
    # 그리고 대입 
    result3 = specialh_short_sym_ex.subs({a : parameters[0][0], b : parameters[0][1], c : parameters[0][2], d : parameters[1][0], e : parameters[1][1], f : parameters[1][2], g : parameters[2][0], h : parameters[2][1], j : parameters[2][2]})
    return result3

def specialh_circuit_long(parameters):
    result4 = specialh_long_sym_ex.subs({a : parameters[0][0], b : parameters[0][1], c : parameters[0][2], d : parameters[1][0], e : parameters[1][1], f : parameters[1][2], g : parameters[2][0], h : parameters[2][1], j : parameters[2][2]})
    return result4

# # sympy 변수 처리하기 
a, b, c, d, e, f, g, h, j = symbols('a, b, c, d, e, f, g, h, j')
#그다음 sympy 형태로 변환하기 -> 시간 오래 걸림 
h_test_short_sym_ex = process_sympy(h_test_short_ex)
h_test_long_sym_ex = process_sympy(h_test_long_ex)
specialh_short_sym_ex = process_sympy(specialh_short_ex)
specialh_long_sym_ex = process_sympy(specialh_long_ex)

#print(had_test_circuit_short([[1, 1, 1], [1, 1, 1], [1, 1, 1]]).evalf())
print("Processing circuit done!")
