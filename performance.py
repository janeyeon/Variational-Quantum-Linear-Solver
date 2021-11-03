import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, transpile, assemble
import random
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from vqls import vqls_calculate_cost_function, apply_fixed_ansatz
from vqls import coefficient_set as vqls_coefficient_set
# import the circuit 

#뽑아주고자 했던 변수를 앞에서 미리 정의한다 
iter = 5
# function for plot
class OpObj(object):
    def __init__(self):
        #맨처음 params의 초기값 
        self.x_0 = [float(random.randint(0,3000))/1000 for i in range(0, 9)]
        #minimize 중간에 뽑아져 나오는 값을 담을 변수
        self.f = np.full(shape=(iter,), fill_value=np.NaN)
        #그걸 f 의 몇번째에 넣을지 계산하는 변수 
        self.count = 0

#뽑아진 obj_fun의 값에다가 중간 param을 넣어서 계산할 값임 
def callback(xk, obj=None):
    obj.f[obj.count] = xk
    obj.count += 1


# fig, ax = plt.subplots(1,1)
x = np.linspace(1,iter, iter)

#====================== for vqls ======================
vqls_op_obj = OpObj()

# cost function 을 minimize 하는 parameter alpha 값을 구한다 (9개)

vqls_out = minimize(vqls_calculate_cost_function, x0= vqls_op_obj.x_0, args=(vqls_op_obj, callback), options={'maxiter':iter}, method="COBYLA")

plt.plot(x, vqls_op_obj.f)

# 여기서 부터는 구한 결과로 비교하는 부분 

# 구한 output 을 쪼갠다  
# 아직 out을 구하지 않은 상황 -> 넣어주어야 함 
out_f = [vqls_out['x'][0:3], vqls_out['x'][3:6], vqls_out['x'][6:9]]

# min parameter 을 이용해서 다시 한번 ansatz 를 계산한다 
circ = QuantumCircuit(3, 3)
apply_fixed_ansatz([0, 1, 2], out_f)
circ.save_statevector()

backend = Aer.get_backend('aer_simulator')

t_circ = transpile(circ, backend)
qobj = assemble(t_circ)
job = backend.run(qobj)

result = job.result()
# 그걸로 확률을 구한다 = |x> 
o = result.get_statevector(circ, decimals=10)

#얘가 실제 coeff 값을 토대로 만든 matrix A = 0.55I + 0.225Z_2 + 0.225Z_3
a1 = vqls_coefficient_set[2]*np.array([[1,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0], [0,0,1,0,0,0,0,0], [0,0,0,1,0,0,0,0], [0,0,0,0,-1,0,0,0], [0,0,0,0,0,-1,0,0], [0,0,0,0,0,0,-1,0], [0,0,0,0,0,0,0,-1]])
a0 = vqls_coefficient_set[1]*np.array([[1,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0], [0,0,-1,0,0,0,0,0], [0,0,0,-1,0,0,0,0], [0,0,0,0,1,0,0,0], [0,0,0,0,0,1,0,0], [0,0,0,0,0,0,-1,0], [0,0,0,0,0,0,0,-1]])
a2 = vqls_coefficient_set[0]*np.array([[1,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0], [0,0,1,0,0,0,0,0], [0,0,0,1,0,0,0,0], [0,0,0,0,1,0,0,0], [0,0,0,0,0,1,0,0], [0,0,0,0,0,0,1,0], [0,0,0,0,0,0,0,1]])
#이게 진짜 최종 matrix A 
a3 = np.add(np.add(a2, a0), a1)
#실제 b의 값 
#이친구 ||b|| 의 값이 1임 ㅋㅋㅋ 
b = np.array([float(1/np.sqrt(8)),float(1/np.sqrt(8)),float(1/np.sqrt(8)),float(1/np.sqrt(8)),float(1/np.sqrt(8)),float(1/np.sqrt(8)),float(1/np.sqrt(8)),float(1/np.sqrt(8))])

#결과 값이 1에 가까울수록 좋음 
# (b * (b' / ||b'||))^2 
print("vqls result: ", (b.dot(a3.dot(o)/(np.linalg.norm(a3.dot(o)))))**2)



#=========== plot =============
plt.show()






