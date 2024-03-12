import numpy as np
from qibo import Circuit, gates, models, callbacks
import qibo

import quimb
import quimb.tensor as qtn

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


qibo.set_backend(backend="qibotn", platform="qutensornet", runcard=computation_settings)

import tebd_eval as evqu

c = Circuit(2)
# Add some gates
c.add(gates.H(0))
c.add(gates.H(1))

result = c()

L = 44
zeros = '0' * ((L - 2) // 3)
binary = zeros + '1' + zeros + '1' + zeros
initial_state =  qtn.MPS_computational_state(binary)

print(evqu.tebd_evol_state_tn_qu(
    initial_state,
    initial_state,
    {"qr_method": False, "svd_method": {"partition": "UV", "abs_cutoff": 1e-12}}, 
    { "H": "<LocalHam1D(L=44, cyclic=False)>", "dt": 1e-3} ))