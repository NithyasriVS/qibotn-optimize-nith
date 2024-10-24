from qibo import Circuit, gates, hamiltonians
from qibo.symbols import X, Y, Z
from qibo.hamiltonians import SymbolicHamiltonian
import qibo
import numpy as np

nqubits = 3
cost_hamiltonian = hamiltonians.XXZ(nqubits)
mixer_hamiltonian = SymbolicHamiltonian(0.5 * X(0) * Z(1) + 1.0 * Y(1) * X(2) + 0.8 * Z(0) * Z(2))

computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": {
        "qr_method": False,
        "svd_method": {
            "partition": "UV",
            "abs_cutoff": 1e-12,
        },
    },
    "NCCL_enabled": False,
    "expectation_enabled": False,
    "QAOA_execute": {
        "ham_cost": cost_hamiltonian,
        "ham_mixer": mixer_hamiltonian,
        "circ_depth": 5,
        "init_params": 0.01 * np.random.random(4),
        "dt": 0.1
    }
}

qibo.set_backend(backend="qibotn", platform="cutensornet", runcard=computation_settings)