import qiskit
import random
import numpy as np
import time
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, transpile, assemble

from scipy.optimize import minimize, show_options

from vqls import apply_fixed_ansatz, coefficient_set
from vqls import calculate_cost_function as vqls_calculate_cost_function

from customVQLS import calculate_cost_function as short_vqls_calculate_cost_function

# ============== 공통적인 값 설정 ================
# 얘가 실제 coeff 값을 토대로 만든 matrix A = 0.45Z_3 + 0.55I
a1 = coefficient_set[1]*np.array([[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [
                                 0, 0, 0, 0, -1, 0, 0, 0], [0, 0, 0, 0, 0, -1, 0, 0], [0, 0, 0, 0, 0, 0, -1, 0], [0, 0, 0, 0, 0, 0, 0, -1]])
a2 = coefficient_set[0]*np.array([[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [
                                 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1]])
# 이게 진짜 최종 matrix A
a3 = np.add(a1, a2)

b = np.array([float(1/np.sqrt(8)), float(1/np.sqrt(8)), float(1/np.sqrt(8)), float(1/np.sqrt(8)),
              float(1/np.sqrt(8)), float(1/np.sqrt(8)), float(1/np.sqrt(8)), float(1/np.sqrt(8))])

show_options(disp = False)

# 뽑아주고자 했던 변수를 앞에서 미리 정의한다
iter = 300
test_num = 100
time_long = 0
time_short = 0
vqls_acc = 0
short_acc = 0
method = "COBYLA"

# function for plot
class OpObj(object):
    def __init__(self, num):
        # 맨처음 params의 초기값
        random.seed(num)
        self.x_0 = [float(random.randint(0, 3000))/1000 for i in range(0, 9)]
        # minimize 중간에 뽑아져 나오는 값을 담을 변수
        self.f = np.full(shape=(iter,), fill_value=np.NaN)
        # 그걸 f 의 몇번째에 넣을지 계산하는 변수
        self.count = 0

# 뽑아진 obj_fun의 값에다가 중간 param을 넣어서 계산할 값임


def callback(xk, obj=None):
    obj.f[obj.count] = xk
    obj.count += 1

x = np.linspace(1, iter, iter)

for num in range(0, test_num):
    print("Current test_num: ", num)
    
    # ====================== for VQLS ======================
    vqls_op_obj = OpObj(num)

    # cost function 을 minimize 하는 parameter alpha 값을 구한다 (9개)

    #print("\n======== VQLS minimization =========\n")

    start_vqls = time.time()

    vqls_out = minimize(vqls_calculate_cost_function, x0=vqls_op_obj.x_0, args=(
        vqls_op_obj, callback), options={'maxiter': iter, 'disp': False}, method= method)

    time_vqls = time.time() - start_vqls

    plt.plot(x, vqls_op_obj.f, label='VQLS version')

    # 여기서 부터는 구한 결과로 비교하는 부분

    # 구한 output 을 쪼갠다
    # 아직 out을 구하지 않은 상황 -> 넣어주어야 함
    vqls_out_f = [vqls_out['x'][0:3], vqls_out['x'][3:6], vqls_out['x'][6:9]]

    # min parameter 을 이용해서 다시 한번 ansatz 를 계산한다
    vqls_circ = QuantumCircuit(3, 3)

    apply_fixed_ansatz([0, 1, 2], vqls_out_f, vqls_circ)
    vqls_circ.save_statevector()

    backend = Aer.get_backend('aer_simulator')

    vqls_t_circ = transpile(vqls_circ, backend)
    vqls_qobj = assemble(vqls_t_circ)
    vqls_job = backend.run(vqls_qobj)

    vqls_result = vqls_job.result()
    # 그걸로 확률을 구한다 = |x>
    vqls_o = vqls_result.get_statevector(vqls_circ, decimals=10)

    # ====================== for short custom VQLS ======================

    short_vqls_op_obj = OpObj(num)

    # cost function 을 minimize 하는 parameter alpha 값을 구한다 (9개)

    #print("\n======== short custom VQLS minimization =========\n")

    start_short_vqls = time.time()

    short_vqls_out = minimize(short_vqls_calculate_cost_function, x0=short_vqls_op_obj.x_0, args=(
        short_vqls_op_obj, callback), options={'maxiter': iter, 'disp': False}, method= method)

    time_short_vqls = time.time() - start_short_vqls

    plt.plot(x, short_vqls_op_obj.f, label='Simplified VQLS version')

    # 여기서 부터는 구한 결과로 비교하는 부분
    # 구한 output 을 쪼갠다
    # 아직 out을 구하지 않은 상황 -> 넣어주어야 함
    short_vqls_out_f = [short_vqls_out['x'][0:3],
                        short_vqls_out['x'][3:6], short_vqls_out['x'][6:9]]

    # min parameter 을 이용해서 다시 한번 ansatz 를 계산한다
    short_vqls_circ = QuantumCircuit(3, 3)
    apply_fixed_ansatz([0, 1, 2], short_vqls_out_f, short_vqls_circ)
    short_vqls_circ.save_statevector()

    backend = Aer.get_backend('aer_simulator')

    short_vqls_t_circ = transpile(short_vqls_circ, backend)
    short_vqls_qobj = assemble(short_vqls_t_circ)
    short_vqls_job = backend.run(short_vqls_qobj)

    short_vqls_result = short_vqls_job.result()
    # 그걸로 확률을 구한다 = |x>
    short_vqls_o = short_vqls_result.get_statevector(
        short_vqls_circ, decimals=10)

# ========= print ============
    print("\n======VQLS RESULT======\n")
    
    print("VQLS Result: ", (b.dot(a3.dot(vqls_o)/(np.linalg.norm(a3.dot(vqls_o)))))**2)
    print("VQLS Calculation time (s) : ", time_vqls)
    time_long += time_vqls
    vqls_acc += (b.dot(a3.dot(vqls_o)/(np.linalg.norm(a3.dot(vqls_o)))))**2

    print("\n======Short Custom VQLS RESULT======\n")

    print("Short Custom VQLS Result: ", (b.dot(a3.dot(short_vqls_o)/(np.linalg.norm(a3.dot(short_vqls_o)))))**2)
    print("Short Custom VQLS Calculation time (s) : ", time_short_vqls)
    time_short += time_short_vqls
    short_acc += (b.dot(a3.dot(short_vqls_o)/(np.linalg.norm(a3.dot(short_vqls_o)))))**2

    print("")
    print("Speedup : ", time_vqls/time_short_vqls)

    # =========== plot =============
    plt.title('VQLS Cost Function Convergence, test_num= ' + str(num))
    plt.xlabel('Number of iteration', labelpad=10)
    plt.ylabel('Cost Function', labelpad=10) #Cost = 1-overall_sum_2/overall_sum_1
    plt.legend()
    #plt.show()
    plt.savefig(method + '_' + str(num) + '.png',dpi=300)
    plt.close()

avg_time_long = time_long/test_num
avg_time_short = time_short/test_num
avg_vqls_result = vqls_acc/test_num
avg_short_result = short_acc/test_num

print("")
print('Total test_num: ', test_num)
print('Average VQLS result: ', avg_vqls_result)
print('Average Simplified_VQLS result: ', avg_short_result)
print('Average VQLS time (s): ',avg_time_long)
print('Average Simplified_VQLS time (s): ',avg_time_short)
print('Average Speedup: ', avg_time_long/avg_time_short)