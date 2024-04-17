import quimb as qmb
import numpy as np
import logging

# this file must provide these things
# 1. a way to extract the hamiltonian unitaries and handle them to be able to pass into TEBD
# 2. the tebd algorithm function(s) which can be called in eval_qu.py file
# the tebd algo itself can use APIs quimb gives so it won't be from scratch 

# pseudocode for tebd



hj = "what exactly - a processed ver of the unitaries"
# of terms_list is passed to this fn when it's called in quimb.py or eval_qu.py, then what is the
# relation between the terms and hj
dt = 1e-2 # in actual get this from the tebd_opts
#u = np.exp(1j * dt * hj) # get this from the circuit so circiut must be passed in as a fn paramter

example_logging = "[EXAMPLE]"
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
# dense vector of final mps
