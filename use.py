import numpy as np
from qibo import Circuit, gates, hamiltonians, models
import qibo

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
        "dt": 1e-3,
        "start": 0,
        "stop": 1.001,
        "opt": "entropy"
    },
    "NCCL_enabled": False,
    "expectation_enabled": False,
}

qibo.set_backend(backend="qibotn", platform="qutensornet", runcard=computation_settings)

ham = hamiltonians.TFIM(nqubits=5, dense=False)
circuit = ham.circuit(dt=1e-2)

nqubits = 5
ham = hamiltonians.TFIM(nqubits=5, dense=False)
circuit = ham.circuit(dt=1e-2)

initial_state = np.ones(2 ** nqubits) / np.sqrt(2 ** nqubits)
evolve = models.StateEvolution(ham, dt=1e-3)
final_state = evolve(final_time=1, initial_state=initial_state)

print(final_state)
