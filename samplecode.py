import qibo
from qibo import Circuit, gates

'''# user defines the number of qubits they want
nqubits = 4
# user defines their hamiltonian using qibo
hamiltonian = hamiltonians.XXZ(nqubits)'''

'''Computation settings for TEBD

    dt: time step for evolution
    opts: physical quantity to evaluate (available options are: entropy, zmag, schmidtgap)
    start
    stop

'''

'''computation_settings = {
        "MPI_enabled": False,
        "MPS_enabled": {
            "qr_method": False,
            "svd_method": {
                "partition": "UV",
                "abs_cutoff": 1e-12,
            },
        },
        "TEBD_enabled": {
            "dt": 1e-3,
            "opts": "entropy",
            "start": 0,
            "stop": 1.001
        },
        "NCCL_enabled": False,
        "expectation_enabled": False
    }'''

computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": {
        "qr_method": False,
        "svd_method": {
            "partition": "UV",
            "abs_cutoff": 1e-12,
        },
    },
    "TEBD_enabled": False,
    "NCCL_enabled": False,
    "expectation_enabled": False,
}

qibo.set_backend(backend="qibotn", platform="qutensornet", runcard=computation_settings)

import numpy as np
from qibo import models, gates, hamiltonians

nqubits = 3

circuit = Circuit(nqubits)
circuit.add(gates.H(0))
circuit.add(gates.H(1))

hamiltonian = hamiltonians.XXZ(nqubits)

result = circuit()
print(result.state())



