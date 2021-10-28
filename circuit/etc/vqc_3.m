syms alpha1 beta1 gamma1 real
syms alpha2 beta2 gamma2 real
syms alpha3 beta3 gamma3 real

syms x1 x2 x3 real

init1 = [cos(x1) sin(x1)];
init2 = [cos(x2) sin(x2)];
init3 = [cos(x3) sin(x3)];

init_p = kron(init1, init2);
init = kron(init_p, init3).';

cnot_1 = kron(CNOT, eye(2));
cnot_2 = kron(eye(2), CNOT);

rotation_p = kron(R(alpha1,beta1,gamma1),R(alpha2,beta2,gamma2));
rotation = kron(rotation_p, R(alpha3,beta3,gamma3));

%result is the output statevector
result = rotation * cnot_2 * cnot_1 * init;

%r is the Prob(0) for the 1st qubit
r = result(1)*conj(result(1)) + result(2)*conj(result(2)) + result(3)*conj(result(3)) + result(4)*conj(result(4))
num_mul(r)

s = simplify(r)
num_mul(s)

%{
for s = 1:1:10
   fprintf('\n');
   steps = s
   expr = simplify(r,s);
   num = num_mul(expr)
end

for s = 10:10:200
   fprintf('\n');
   steps = s
   expr = simplify(r,s);
   num = num_mul(expr)
end
%}

s_10 = simplify(r,10)
num_mul(s_10)

s_30 = simplify(r,30)
num_mul(s_30)

s_50 = simplify(r,50)
num_mul(s_50)

s_100 = simplify(r,100)
num_mul(s_100)

s_200 = simplify(r,200)
num_mul(s_200)

save('result.mat', r, s_10, s_30, s_50, s_100, s_200)

%%
d_a1_0 = diff(r,alpha1)
d_b1_0 = diff(r,beta1)
d_g1_0 = diff(r,gamma1)

d_a2_0 = diff(r,alpha2)
d_b2_0 = diff(r,beta2)
d_g2_0 = diff(r,gamma2)

d_a3_0 = diff(r,alpha3)
d_b3_0 = diff(r,beta3)
d_g3_0 = diff(r,gamma3)


d_a1 = diff(s_200,alpha1)
d_b1 = diff(s_200,beta1)
d_g1 = diff(s_200,gamma1)

d_a2 = diff(s_200,alpha2)
d_b2 = diff(s_200,beta2)
d_g2 = diff(s_200,gamma2)

d_a3 = diff(s_200,alpha3)
d_b3 = diff(s_200,beta3)
d_g3 = diff(s_200,gamma3)

%% 
% 

function Rx = Rx(theta)
    Rx = [cos(theta/2) -isin(theta/2);
          -isin(theta/2) cos(theta/2)];
end 

function Ry = Ry(theta)
    Ry = [cos(theta/2) -sin(theta/2);
          sin(theta/2) cos(theta/2)];
end

function Rz = Rz(theta)
    Rz = [exp(-1i*theta/2) 0;
          0 exp(1i*theta/2)];
end

function R = R(a,b,c)
    R = Rz(a)*Ry(b)*Rz(c);
end

function CNOT = CNOT()
    CNOT = [1 0 0 0;
        0 1 0 0;
        0 0 0 1;
        0 0 1 0];
end

function num_mul = num_mul(A)
    num_mul = numel(regexp(char(A), '[*]'));
end

function disp_msg_var(msg, v)
  disp([msg inputname(2)]);
end
