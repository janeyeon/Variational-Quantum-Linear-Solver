import sys
import os
from timeit import default_timer as clock

from symengine import *
import sympy
from process_latex import process_sympy
 
def run_benchmark(n):
    #a0 = symbols("a0")
    #a1 = symbols("a1")
    a, b, c, d, e, f, g, h, j = sympy.symbols('a, b, c, d, e, f, g, h, j')
    #exp = (((((sin(j)*cos(f))*cos(e))*cos(d))*sin(c))*cos(b) + ((-sin(b)*sin(e)*sin(j)*cos(d)*cos(f) + sin(f)*cos(j))*sin(c))*cos(a) - ((((sin(b)*sin(e) - cos(a)*cos(b)*cos(e))*sin(j))*sin(f))*cos(d) + cos(f)*cos(j))*cos(c) - sin(a)*sin(d)*sin(f)*sin(j)*cos(e) + 1)/2
    exp_tex = "\\frac{1}{2}( {{{\cos( a )}{\sin( c )}( {{{\sin( f )}{\cos( j )}} - {{\sin( b )}{\cos( d )}{\sin( e )}{\cos( f )}{\sin( j )}}} )} - {{\cos( c )}( {{{\cos( d )}{\sin( f )}{\sin( j )}( {{{\sin( b )}{\sin( e )}} - {{\cos( a )}{\cos( b )}{\cos( e )}}} )} + {{\cos( f )}{\cos( j )}}} )} - {{\sin( a )}{\sin( d )}{\cos( e )}{\sin( f )}{\sin( j )}} + {{\cos( b )}{\sin( c )}{\cos( d )}{\cos( e )}{\cos( f )}{\sin( j )}} + 1} )"
    exp = process_sympy(exp_tex)
    """
    f = 0;
    for i in range(2, n):
        s = symbols("a%s" % i)
        e = e + sin(s)
        f = f + sin(s)
    f = -f
    """

    t1 = clock()
    print(exp)
    print("")

    #exp = exp.xreplace({a: 1, b:2, c: 1, d:1, e:1, f:1,g:1,h:1, j:1})
    a0, b0, c0, d0, e0, f0, g0, h0, j0 = symbols('a0, b0, c0, d0, e0, f0, g0, h0, j0')

    exp = exp.xreplace({a: a0, b: b0, c: c0, d: d0, e: e0, f: f0, g: g0, h: h0, j: j0})

    exp = exp.subs({a0: 1, b0:2, c0: 1, d0:1, e0:1, f0:1, g0:1, h0:1, j0:1})

    print(exp)

    #e = expand(e)
    #print(e)

    t2 = clock()
    print("%s ms" % (1000 * (t2 - t1)))
 
if __name__ == '__main__':
    n=100
    run_benchmark(n)