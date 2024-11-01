import qibo
from qibo import Circuit, gates, hamiltonians, models
import numpy as np

computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": False,
    "NCCL_enabled": False,
    "expectation_enabled": False,
    "VQE_execute": True
}


qibo.set_backend(backend="qibotn", platform="cutensornet", runcard=computation_settings)

nqubits = 2
c = Circuit(nqubits)
for i in range(0, nqubits):
    c.add(gates.RX(i,0))

hamiltonian = hamiltonians.XXZ(nqubits)
initial_parameters = 0.01 * np.random.random(nqubits)

vqe = models.VQE(c, hamiltonian)
vqe.minimize(initial_parameters)

c=vqe.circuit

result = c()
print(result.state())