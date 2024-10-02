from qibo import Circuit, gates, hamiltonians
from qibo.symbols import X, Y, Z
from qibo.hamiltonians import SymbolicHamiltonian
import qibo

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
        "gamma": 2,
        "beta": 1 
    }
}

qibo.set_backend(backend="qibotn", platform="cutensornet", runcard=computation_settings)

c = Circuit(nqubits)

# uniform superposition state preparation circuit
for i in range(0, nqubits):
    c.add(gates.H(i))

result = c()

print(result.state())