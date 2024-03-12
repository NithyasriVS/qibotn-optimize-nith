import quimb
import quimb.tensor as qtn

L = 44
zeros = '0' * ((L - 2) // 3)
binary = zeros + '1' + zeros + '1' + zeros
print('psi0:', f"|{binary}>")

psi0 = qtn.MPS_computational_state(binary)

H = qtn.ham_1d_heis(L)

tebd = qtn.TEBD(psi0, H)

tebd.split_opts['cutoff'] = 1e-12

be_t_b = []

import numpy as np
ts = np.linspace(0, 80, 101)
for psit in tebd.at_times(ts, tol=1e-3):
    
    be_b = []
    
    for j in range(1, L):
        # after which we only need to move it from previous site

        be_b += [psit.entropy(j, cur_orthog=j)]

    be_t_b += [be_b]

print(be_t_b)

