import quimb as qmb
import numpy as np

# this file must provide these things
# 1. a way to extract the hamiltonian unitaries and handle them to be able to pass into TEBD
# 2. the tebd algorithm function(s) which can be called in eval_qu.py file
# the tebd algo itself can use APIs quimb gives so it won't be from scratch 

# pseudocode for tebd

hj = "what exactly - a processed ver of the unitaries"
dt = 1e-2 # in actual get this from the tebd_opts
u = np.exp(1j * dt * hj) # get this from the circuit so circiut must be passed in as a fn paramter

# unitaries -> internally commuting parts
# individually exponentiate the parts

# ???

# apply U repeatedly as per time interval
# final mps after evol
# dense vector of final mps
