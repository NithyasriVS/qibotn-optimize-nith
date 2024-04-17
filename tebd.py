import quimb as qmb
import numpy as np
import logging

# this file must provide these things
# 1. a way to extract the hamiltonian unitaries and handle them to be able to pass into TEBD
# 2. the tebd algorithm function(s) which can be called in eval_qu.py file
# the tebd algo itself can use APIs quimb gives so it won't be from scratch 

# pseudocode for tebd algo (my current ustanding only): highlighted main words not ustd using ""

'''
# Step 1: Construct an evolution operator by splitting H into "internally commuting parts"

# Step 2: Exponentiate each summand of each part individually (exponentiate acc to which formula?)

# Step 3: If the summands are "non-local", swap gates to be introduced before and after exp

        Step 2 or Step2&3 give MPO component tensors at outcome

# Step 4: "Place" these tensors within MPO spanning entire system which gives us Ua

# Step 5: Do SVD of Ua 

# Step 6: Do SVD again on Ua but now the delta = delta/2 where delta = total step, in the
          initial exponentiation

# Step 7: Append the reversed list of MPOs to itself so that new U = {U1, U2, U3, U3, U2, U1}

# Step 8: Now, to actually do the evolution of the ""state", keep "applying" U to the state, 
          each time advancing the state by delta time
'''

hj = "internally commuting part"
# of terms_list is passed to this fn when it's called in quimb.py or eval_qu.py, then what is the
# relation between the terms and hj
dt = 1e-2 # in actual get this from the tebd_opts
#u = np.exp(1j * dt * hj) # get this from the circuit so circiut must be passed in as a fn paramter

logging.basicConfig(filename="tebd.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

dense_vector_after_every_dt = 5 # dummy value just for now
logger = logging.getLogger()

 
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)
 
# Test messages
#logger.debug("Harmless debug Message")
logger.info("Just an information")
#logger.warning("Its a Warning")
#logger.error("Did you try to divide by zero")
#logger.critical("Internet is down")

# unitaries -> internally commuting parts
# individually exponentiate the parts

# ???

# apply U repeatedly as per time interval
# final mps after evol

# interesting point and potential challenge here:
''' 
how are we gonna reconstruct this as a quimb CircuitMPS object so that .to_dense can be used to
get the dense vector?

and at different dts until total time, I wanna log these dense vector values and only return the
dense vector value of the final mps - DOES THIS EVEN MAKE SENSE AND IS IT DOABLE?
'''
# dense vector of final mps
