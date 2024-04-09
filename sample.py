
import numpy as np
from qibo import Circuit, gates, hamiltonians
import qibo

computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": False,
    "NCCL_enabled": False,
    "expectation_enabled": False
}

qibo.set_backend(backend="qibotn", platform="qutensornet", runcard=computation_settings)

#ham = hamiltonians.TFIM(nqubits=5, dense=False)
ham = hamiltonians.XXZ(nqubits=5, dense=False)
circuit = ham.circuit(dt=1e-2)

result = circuit()

print(result.state())

