import numpy as np
import math
import sympy as sym
import sympy.parsing.sympy_parser as sp

class quantum_computer:
    def __init__(self, n):
        self.n = n
        #크기가 2 ** n 짜리 diagonal matrix 생성 
        # self.mat = np.eye(2 ** n, dtype='complex')
        self.mat = sym.eye(2 ** n)
        ind = []

        #symbol 형태로 바꿔주는 부분 
        self.alpha = sym.symbols("alpha0:%d"%n)
        self.beta = sym.symbols("beta0:%d"%n)
        self.gamma = sym.symbols("gamma0:%d"%n)

        #ai, bi 들도 전부 형태를 한번씩 바꾸어주자 
        self.a = sym.symbols("a0:%d"%n)
        self.b = sym.symbols("b0:%d"%n)

        #string 으로 죄다 저장해서 ind에 넣어놓는 것 -> 이걸 우리의 result 에 넣어놓도록 바꾸어야 한다 
        for i in range(2 ** n):
            tmp = ""
            for j in range(n):
                if j % n != 0: 
                    tmp = ' * ' + tmp
                if (i >> j) % 2 == 1:
                    #tmp = ('(b' + str(n - j) + ')') + tmp
                    tmp = ('b' + str(n-j-1)) + tmp
                else:
                    #tmp = ('(a' + str(n - j) + ')') + tmp
                    tmp = ('a' + str(n-j-1)) + tmp
                
            ind.append(tmp)
        #ind에 각 state에 해당하는 값을 전부 a1 * a2 *..* an 식으로 붙여서 list 생성 
        self.ind = ind 
   
    def result(self, verbose=True):
        myresult = []
        # transformations = sp.standard_transformations + (sp.function_exponentiation,)
        for i in range(2 ** self.n):
            flag = 0
            #매 줄 시작전에 초기화 시켜줌  
            temp_cal = ""
            if verbose == False:
                print(np.round(self.mat[i], 2))
                #print(self.mat[i])
            else:
                for j in range(2 ** self.n):
                    if self.mat[i][j] != 0:
                        if(flag == 0):
                            flag = 1
                        else:
                            # print(" + ", end='')
                            temp_cal += " + "
                        # print("{0:.2f} {1:}".format(self.mat[i][j], self.ind[j]), end="")
                        temp_cal += "({0:.2f}) * {1:}".format(self.mat[i][j], self.ind[j])
                # print()
                myresult.append(temp_cal)
                sym.pprint(sp.parse_expr(temp_cal, evaluate = True))

                # sym.pprint(sp.parse_expr(temp_cal, transformations = transformations))
        print()

    def special_result(self) : 
        #맨처음 special_result를 초기화 
        special_result = [""] * self.n
        myresult = []
        for i in range(2 ** self.n) :
            flag = 0
            temp_cal = ""
            for j in range(2 ** self.n):
                    if self.mat[i][j] != 0:
                        if(flag == 0):
                            flag = 1
                        else:
                            temp_cal += " + "
                        temp_cal += "({0:.2f}) * {1:}".format(self.mat[i][j], self.ind[j])
            myresult.append(temp_cal)
        # 먼저 result 가 선행되어야함 
        
        for i in range(2 ** self.n): 
            for j in range(self.n) : 
                if (i >> j) % 2 == 0 :
                    # 맨 처음 결과를 쓰는 거라면 
                    if special_result[self.n - j - 1] == "": 
                        special_result[self.n - j - 1] = "(" + myresult[i] + ")" + "** 2"
                    else :
                        special_result[self.n - j - 1] = "(" + myresult[i] + ")" + "** 2 + " + special_result[self.n - j - 1]
        
        # for i in range(self.n) :
        #     print("<a" + str(i) + ">")
        #     # print(special_result[i])
        #     sym.pprint(sp.parse_expr(special_result[i], evaluate = True))
        #     print()
        return sp.parse_expr(special_result[0], evaluate = True)


    def really_special_result(self) :
        really_special_result = [""] * self.n
        myresult = []
        for i in range(2 ** self.n) :
            flag = 0
            temp_cal = ""
            for j in range(2 ** self.n):
                if self.mat[i, j] != 0:
                    if(flag == 0):
                        flag = 1
                    else:
                        temp_cal += " + "
                    # temp_cal += "({0:.2f}) * {1:}".format(self.mat[i, j], self.ind[j])
                    temp_cal += str(self.mat[i, j])+ '*' +  str(self.ind[j])
            myresult.append(temp_cal)
        # 먼저 result 가 선행되어야함 
        
        for i in range(2 ** self.n): 
            for j in range(self.n) : 
                if (i >> j) % 2 == 0 :
                    # 맨 처음 결과를 쓰는 거라면 
                    if really_special_result[self.n - j - 1] == "": 
                        really_special_result[self.n - j - 1] = "(" + myresult[i] + ")" + "** 2"
                    else :
                        really_special_result[self.n - j - 1] = "(" + myresult[i] + ")" + "** 2 + " + really_special_result[self.n - j - 1]
                

        for i in range(self.n) :
            print("<a" + str(i) + ">")
            # sym.pprint(sp.parse_expr(really_special_result[i], evaluate = True))

            # 우선 결과를 풀어서 string형태로 저장한다 
            a = str(sym.expand(really_special_result[i]))

            for j in range(self.n) : 
                tempA = "b" + str(j) + "**2"
                tempB = "(1 - a" + str(j) + "**2)"
                #그 다음 b^2 의 값을 1- a^2로 치환한다  
                a = a.replace(tempA, tempB)

            # 이후 공식을 간편하게 하고 출력한다 
            sym.pprint(sym.simplify(a))
            print()
        # expand 먼저 시키고 


   # 이건 alpha, beta, gamma 값을 변수로 생각해서 계산한 방법
    def k_plus(self, i, a) :
        if a :
            return sym.cos(self.alpha[i] / 2) + sym.sin(self.alpha[i] / 2)
        else :
            return sym.cos(self.gamma[i] / 2) + sym.sin(self.gamma[i] / 2)

    def k_minus(self, i, a) :
        if a :
            return sym.cos(self.alpha[i] / 2) - sym.sin(self.alpha[i] / 2)
        else :
            return sym.cos(self.gamma[i] / 2) - sym.sin(self.gamma[i] / 2)

    def real_r(self, i, entry_num) :
        if i >= self.n:
            print("Overflow!")
            return 
        if entry_num == 0 : 
            # (0, 0)
            return sym.cos(self.beta[i] / 2) * self.k_minus(i, True) * self.k_minus(i, False)
        elif entry_num == 1 :
            #(0, 1)
            return sym.sin(self.beta[i] / 2) * 1j * self.k_minus(i, True) * self.k_plus(i, False)
        elif entry_num == 2 :
            #(1, 0)
            return -sym.sin(self.beta[i] / 2) * 1j * self.k_plus(i, True) * self.k_minus(i, False)
        elif entry_num == 3 : 
            #(1, 1)
            return sym.cos(self.beta[i] / 2) * self.k_plus(i, True) * self.k_plus(i, False)
    
    # 수식으로는 : real_r_gate를 선언하면 mat에서 i번째에 해당하는 열에 real_r의 계산값을 추가함 
    # 공식상에서는 : i번째 qubit 에 대해 
    def real_r_gate(self, i) :
        if i >= self.n :
            print("Overflow!")
            return
        l = 2 ** (self.n - i - 1)
        t = 0
        while(t < 2 ** self.n) :
            for k in range(t, t+l) :
                tmp = np.copy(self.mat[k] * self.real_r(i, 0) + self.mat[l + k] * self.real_r(i, 2) )
                self.mat[l + k] = np.copy(self.mat[k] * self.real_r(i, 1) + self.mat[l + k] * self.real_r(i, 3))
                self.mat[k] = tmp 
                print(tmp)
            t += 2 * l
         
    def output(self, l=0):        
        for elem in self.mat[:, l]:
            print(np.round(elem, 3))
        print()
    
    def marginal(self, l=0):
        print("\t\tProb 0\tProb 1")
        for num in range(self.n):
            print(num, "Qubit:\t", end='')
            count = 0
            for i in range(2 ** self.n):
                if i & (1 << num) == 0:
                    count += self.mat[i, l] * np.conjugate(self.mat[i, l])
            if np.imag(count) != 0:
                print("Wrong")
                return
            count = np.real(count)
            print(np.round(count, 3), "\t", np.round(1-count, 3))
                    
    def r(self, a, b, c):
        pauli_z = np.array([[1, 0], [0, -1]])
        pauli_y = np.array([[0, -1j], [1j, 0]])
        
        r_1 = np.cos(a/2) * np.identity(2) - 1j * np.sin(a/2) * pauli_z
        r_2 = np.cos(b/2) * np.identity(2) - 1j * np.sin(b/2) * pauli_y
        r_3 = np.cos(c/2) * np.identity(2) - 1j * np.sin(c/2) * pauli_z 

        temp_res = np.matmul(r_1, r_2)
    
        return np.matmul(temp_res, r_3) 

    def r_gate(self, i, a, b, c): 
        if i >= self.n :
            print("Overflow!")
            return
        l = 2 ** (self.n - i - 1)
        t = 0
        r = self.r(a, b, c)
        while(t < 2 ** self.n):
            for k in range(t, t+l):
                tmp = np.copy(self.mat[k] * r[0][0] + self.mat[l + k] * r[1][0] )
                self.mat[l + k] = np.copy(self.mat[k] * r[0][1] + self.mat[l + k] * r[1][1])
                self.mat[k] = tmp 
                # tmp = np.copy(self.mat[k] * r[0][1] + self.mat[l + k] * r[1][1])
                # self.mat[l + k] = np.copy(self.mat[k] * r[0][0] + self.mat[l + k] * r[1][0] ) 
                # self.mat[k] = tmp 
            t += 2 * l
        # print(r)

    def h(self, a):
        if a >= self.n:
            print("Overflow!")
            return
        
        l = 2 ** a
        t = 0
        while(t < 2 ** self.n):
            for i in range(t, t+l):
                tmp = np.copy(self.mat[i] + self.mat[l + i]) * (0.5 ** 0.5)
                self.mat[l + i] = np.copy(self.mat[i] - self.mat[l + i]) * (0.5 ** 0.5)
                self.mat[i] = tmp
            t += 2 * l
            
    def x(self, a):
        if a >= self.n:
            print("Overflow!")
            return
        
        l = 2 ** a
        t = 0
        while(t < 2 ** self.n):
            for i in range(t, t+l):
                tmp = np.copy(self.mat[l + i])
                self.mat[l + i] = np.copy(self.mat[i])
                self.mat[i] = tmp
            t += 2 * l
            
    def y(self, a):
        if a >= self.n:
            print("Overflow!")
            return
        
        l = 2 ** a
        t = 0
        while(t < 2 ** self.n):
            for i in range(t, t+l):
                tmp = complex(0, -1) * np.copy(self.mat[l + i])
                self.mat[l + i] = complex(0, 1) * np.copy(self.mat[i])
                self.mat[i] = tmp
            t += 2 * l
            
    def z(self, a):
        if a >= self.n:
            print("Overflow!")
            return
        
        l = 2 ** a
        t = 0
        while(t < 2 ** self.n):
            for i in range(t, t+l):
                self.mat[l + i] = -np.copy(self.mat[l + i])
            t += 2 * l
            
    def phase(self, a, theta):
        if a >= self.n:
            print("Overflow!")
            return
        
        l = 2 ** a
        t = 0
        while(t < 2 ** self.n):
            for i in range(t, t+l):
                self.mat[l + i] = np.copy(self.mat[l + i]) * (math.e ** (1j * theta))
            t += 2 * l
    """
    def cnot(self, control, target):
        if control >= self.n or target >= self.n:
            print("Overflow!")
            return
        
        for i in range(2 ** self.n):
            if i & (1 << control) != 0:
                if i & (1 << target) == 0:
                    tmp = np.copy(self.mat[i | (1 << target)])
                    self.mat[i | (1 << target)] = np.copy(self.mat[i])
                    self.mat[i] = tmp
    """
    def cnot(self, control, target):
    
        if len(control) >= (self.n) or target >= self.n:
            print("Overflow!")
            return
        
        l = []
        for elem in control:
            l.append(1 << elem)
        
        for i in range(2 ** self.n):
            flag = 0
            for elem in l:
                if i & elem == 0:
                    flag = 1
            if flag == 0:
                if i & (1 << target) == 0:
                    tmp = np.copy(self.mat[i | (1 << target)])
                    self.mat[i | (1 << target)] = np.copy(self.mat[i])
                    self.mat[i] = tmp
    
    def init(self, vector):
        #vector 는 x와 y를 concat 한 결과 
        if math.ceil(np.log2(len(vector))) + 1 != self.n:
            print("size error!")
            return
        
        
        
    