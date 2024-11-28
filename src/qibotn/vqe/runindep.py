import qibo
from qibo import models, hamiltonians, Circuit, gates
import numpy as np
from vqe_tn import run_vqe

computation_settings = {
            "MPI_enabled": False,
            "MPS_enabled": False,
            "NCCL_enabled": False,
            "expectation_enabled": False
}

qibo.set_backend(backend="qibotn", platform="cutensornet", runcard=computation_settings)

nqubits = 4
c = Circuit(nqubits)
for i in range(0, nqubits):
    c.add(gates.RX(i,0))

initial_parameters = 0.01 * np.random.random(nqubits)

ham = hamiltonians.XXZ(nqubits)

vqe_circuit = run_vqe(c, ham, initial_parameters)
result = vqe_circuit()
print(result.state())

