import quimb as qmb
import numpy as np

# pseudocode for tebd

dt = 1e-2
u = np.exp(1j * dt)

# unitaries -> internally commuting parts
# individually exponentiate the parts
# ???
# apply U repeatedly as per time interval
# final mps after evol
# dense vector of final mps
