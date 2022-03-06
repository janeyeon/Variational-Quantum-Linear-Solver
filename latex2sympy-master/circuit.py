import sys
import time

from sympy import *
#from symengine import *
from sympy.core.symbol import symbols
from process_latex import process_sympy
from dataExtraction import h_test_short, h_test_long, specialh_long_I, specialh_short_I, specialh_long_Z3, specialh_short_Z3

def had_test_circuit_short(parameters): 
    #result = h_test_short_sym.xreplace({a : parameters[0][0], b : parameters[0][1], c : parameters[0][2], d : parameters[1][0], e : parameters[1][1], f : parameters[1][2], g : parameters[2][0], h : parameters[2][1], j : parameters[2][2]})
    result = f_h_test_short(parameters[0][0], parameters[0][1], parameters[0][2], parameters[1][0], parameters[1][1], parameters[1][2], parameters[2][0], parameters[2][1], parameters[2][2])
    # result = h_test_short_sym_ex.subs({a : parameters[0][0], b : parameters[1][0], c : parameters[2][0], d : parameters[0][1], e : parameters[1][1], f : parameters[2][1], g : parameters[0][2], h : parameters[1][2], i : parameters[2][2]})
    return result

def had_test_circuit_long(parameters): 
    #result2 = h_test_long_sym.xreplace({a : parameters[0][0], b : parameters[0][1], c : parameters[0][2], d : parameters[1][0], e : parameters[1][1], f : parameters[1][2], g : parameters[2][0], h : parameters[2][1], j : parameters[2][2]})
    result2 = f_h_test_long(parameters[0][0], parameters[0][1], parameters[0][2], parameters[1][0], parameters[1][1], parameters[1][2], parameters[2][0], parameters[2][1], parameters[2][2])
    return result2

def specialh_circuit_short_I(parameters): 
    #result3 = specialh_short_sym_I.xreplace({a : parameters[0][0], b : parameters[0][1], c : parameters[0][2], d : parameters[1][0], e : parameters[1][1], f : parameters[1][2], g : parameters[2][0], h : parameters[2][1], j : parameters[2][2]})
    result3 = f_specialh_short_I(parameters[0][0], parameters[0][1], parameters[0][2], parameters[1][0], parameters[1][1], parameters[1][2], parameters[2][0], parameters[2][1], parameters[2][2])
    return result3

def specialh_circuit_long_I(parameters):
    #result4 = specialh_long_sym_I.xreplace({a : parameters[0][0], b : parameters[0][1], c : parameters[0][2], d : parameters[1][0], e : parameters[1][1], f : parameters[1][2], g : parameters[2][0], h : parameters[2][1], j : parameters[2][2]})
    result4 = f_specialh_long_I(parameters[0][0], parameters[0][1], parameters[0][2], parameters[1][0], parameters[1][1], parameters[1][2], parameters[2][0], parameters[2][1], parameters[2][2])
    return result4

def specialh_circuit_short_Z3(parameters): 
    #result5 = specialh_short_sym_Z3.xreplace({a : parameters[0][0], b : parameters[0][1], c : parameters[0][2], d : parameters[1][0], e : parameters[1][1], f : parameters[1][2], g : parameters[2][0], h : parameters[2][1], j : parameters[2][2]})
    result5 = f_specialh_short_Z3(parameters[0][0], parameters[0][1], parameters[0][2], parameters[1][0], parameters[1][1], parameters[1][2], parameters[2][0], parameters[2][1], parameters[2][2])
    return result5

def specialh_circuit_long_Z3(parameters):
    #result6 = specialh_long_sym_Z3.xreplace({a : parameters[0][0], b : parameters[0][1], c : parameters[0][2], d : parameters[1][0], e : parameters[1][1], f : parameters[1][2], g : parameters[2][0], h : parameters[2][1], j : parameters[2][2]})
    result6 = f_specialh_short_Z3(parameters[0][0], parameters[0][1], parameters[0][2], parameters[1][0], parameters[1][1], parameters[1][2], parameters[2][0], parameters[2][1], parameters[2][2])
    return result6

sys.setrecursionlimit(10000)

# # sympy 변수 처리하기 
a, b, c, d, e, f, g, h, j = symbols('a, b, c, d, e, f, g, h, j')

start = time.time()

#그다음 sympy 형태로 변환하기 -> 시간 오래 걸림 
h_test_short_sym = process_sympy(h_test_short)
f_h_test_short = lambdify([a, b, c, d, e, f, g, h, j], h_test_short_sym)

specialh_short_sym_I = process_sympy(specialh_short_I)
f_specialh_short_I = lambdify([a, b, c, d, e, f, g, h, j], specialh_short_sym_I)

specialh_short_sym_Z3 = process_sympy(specialh_short_Z3)
f_specialh_short_Z3 = lambdify([a, b, c, d, e, f, g, h, j], specialh_short_sym_Z3)

print("Processing Short done!")

# h_test_long_sym = process_sympy(h_test_long)
# f_h_test_long = lambdify([a, b, c, d, e, f, g, h, j], h_test_long_sym)

# specialh_long_sym_I = process_sympy(specialh_long_I)
# f_specialh_long_I = lambdify([a, b, c, d, e, f, g, h, j], specialh_long_sym_I)

# specialh_long_sym_Z3 = process_sympy(specialh_long_Z3)
# f_specialh_long_Z3 = lambdify([a, b, c, d, e, f, g, h, j], specialh_long_sym_Z3)

# print("Processing Long done!")

print("Processing circuit done!")

print("Processing time (s): ", time.time() - start)
