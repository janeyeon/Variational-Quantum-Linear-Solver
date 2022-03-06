from sympy import *
import numpy
import time
from sympy.printing.aesaracode import aesara_function

x, y, z = symbols('x, y, z')
expr = (x**z + y**z)**(1/z)

f_lambdify = lambdify([x,y,z], expr)
f_aesara = aesara_function([x,y,z], [expr])

start = time.time()
for i in range(1,2):
    f_lambdify(3,4,2)
print(time.time()-start)

start = time.time()
for i in range(1,2):
    f_aesara(3,4,2)
print(time.time()-start)

