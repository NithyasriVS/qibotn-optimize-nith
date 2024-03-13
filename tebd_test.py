import numpy as np
from qibo import Circuit, gates
import qibo

import quimb
import quimb.tensor as qtn

#import qibotn_dependency as qd
from qibotn import eval_qu as evqu

computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": {
        "qr_method": False,
        "svd_method": {
            "partition": "UV",
            "abs_cutoff": 1e-12,
        },
    },
    "TEBD_enabled": {
        "H": qtn.ham_1d_heis(44),
        "dt": 1e-3
    },
    "NCCL_enabled": False,
    "expectation_enabled": False,
}
import qibo
from qibo import gates, models

'''circuit = models.Circuit(44)

# Apply X gates to flip the qubits in the 14th and 29th positions
circuit.add(gates.X(14))
circuit.add(gates.X(29))

result = circuit()

state = result.state()'''

qibo.set_backend(backend="qibotn", platform="qutensornet", runcard=computation_settings)

circuit = models.Circuit(20)

# Apply X gates to flip the qubits in the 15th and 29th positions
circuit.add(gates.X(8))
circuit.add(gates.X(18))


#c = Circuit(2)

#c.add(gates.H(0))
#c.add(gates.H(1))



result = circuit()

print(result.state())


'''print(evqu.tebd_evol_state_tn_qu(
    initial_state,
    initial_state,
    {"qr_method": False, "svd_method": {"partition": "UV", "abs_cutoff": 1e-12}}, 
    { "H": "<LocalHam1D(L=44, cyclic=False)>", "dt": 1e-3} ))'''



