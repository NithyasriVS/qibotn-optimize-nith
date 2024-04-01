import numpy as np
from qibo import Circuit, gates, hamiltonians, models, callbacks
import qibo

computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": False,
    "TEBD_enabled": {
        "dt": 1e-3,
        "start": 0,
        "stop": 1.001,
        "opt": "entropy"
    },
    "NCCL_enabled": False,
    "expectation_enabled": False,
}

qibo.set_backend(backend="qibotn", platform="qutensornet", runcard=computation_settings)

nqubits = 5
dt = 1e-3

ham = hamiltonians.TFIM(nqubits=nqubits, dense=False)
c = ham.circuit(dt=dt)

entropy = c()

print(entropy)





