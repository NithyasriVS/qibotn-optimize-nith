from qibo import models, hamiltonians, Circuit, gates
import numpy as np
from qibo.symbols import X, Y, Z
import qibo

computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": False,
    "NCCL_enabled": False,
    "expectation_enabled": False
}
qibo.set_backend(backend="qibotn", platform="qutensornet", runcard=computation_settings)

''' Circuit is exposed only if hamiltonian is SymbolicHamiltonian
hamiltonian = sum([X(0) * X(1), Y(0) * Y(1), 0.5 * Z(0) * Z(1)])
hamiltonian = hamiltonians.SymbolicHamiltonian(hamiltonian)
initial_parameters = 0.01 * np.random.random(4)
q_m = models.QAOA(hamiltonian)
best_energy, final_parameters, extra = q_m.minimize(initial_parameters, method="BFGS")
c = q_m.hamiltonian.circuit(dt=0.1)
'''

# VQE works when running vqe.circuit on Qibotn (tried with quimb platform)
vqe_ansatz = models.Circuit(2)
vqe_ansatz.add(gates.RY(0, theta=0))
hamiltonian = hamiltonians.XXZ(2)
initial_parameters = np.random.uniform(0, 2, 1)

v_m = models.VQE(vqe_ansatz, hamiltonian)
v_m.minimize(initial_parameters)
c = v_m.circuit

result = c()

print(result.state())




