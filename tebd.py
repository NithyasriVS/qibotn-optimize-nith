import quimb as qmb
import numpy as np

# pseudocode for tebd

dt = 1e-2
np.exp(1j * dt)

# unitaries -> internally commuting parts
# exponentiate the part individually
# product them to get an MPO
# svd decompose MPO
# repeat svd
# apply U repeatedly as per time interval
# final mps after evol
# dense vector of final mps
