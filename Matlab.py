import matlab.engine
import numpy as np
from numpy import array, arange
from matlab import double as double_m

eng = matlab.engine.start_matlab()
eng.desktop(nargout=0)

eng.workspace['x'] = 3
a = eng.eval("x+3;")

eng.eval("y = 5;", nargout=0)
print(eng.workspace['y'])