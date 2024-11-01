import qibo
from qibo import models, Circuit, hamiltonians, gates

import numpy as np

computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": False,
    "NCCL_enabled": False,
    "expectation_enabled": False
}

qibo.set_backend(backend="qibotn", platform="qutensornet", runcard=computation_settings)

nqubits = 2
problem_hamiltonian = hamiltonians.XXZ(nqubits)

circuit = Circuit(nqubits)
for i in range(0, nqubits):
    circuit.add(gates.RX(i,0))

initial_parameters = 0.01 * np.random.random(nqubits)
vqe = models.VQE(circuit, problem_hamiltonian)
print(vqe.minimize(initial_parameters))

nqubits=3
from qibo.symbols import X, Y, Z
problem_hamiltonian = hamiltonians.SymbolicHamiltonian(sum([X(0) * X(1), Y(0) * Y(1), 0.5 * Z(0) * Z(1)]))

params = 0.01 * np.random.random(nqubits)
qaoa = models.QAOA(problem_hamiltonian, mixer=None)
best_energy, final_parameters, extras = qaoa.minimize(initial_parameters)
print(final_parameters)