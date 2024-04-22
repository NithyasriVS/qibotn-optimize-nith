import quimb as qu
import quimb.tensor as qtn
import numpy as np

L = 5
binary = '00000'
psi0 = qtn.MPS_computational_state(binary)


H = qtn.ham_1d_heis(L)

tebd = qtn.TEBD(psi0, H)

# Since entanglement will not grow too much, we can set quite
#     a small cutoff for splitting after each gate application
tebd.split_opts['cutoff'] = 1e-12
psi0.show()  # prints ascii representation of state
