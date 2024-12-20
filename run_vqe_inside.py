import traceback
import qibo
from qibo.result import QuantumState
from qibo import Circuit, gates, hamiltonians, models
from qibo.symbols import Z
import numpy as np
import sys

nqubits = 4

#try:
computation_settings = {
            "MPI_enabled": False,
            "MPS_enabled": False,
            "NCCL_enabled": False,
            "expectation_enabled": False,
            "VQE_execute": {"hamiltoninan": "XXZ", "initial_parameters": 0.01 * np.random.random(nqubits)}
}

qibo.set_backend(backend="qibotn", platform="cutensornet", runcard=computation_settings)

# user gives hamiltonian in runcard and only has to get started with the ansatz
'''
    c = Circuit(nqubits)
    for i in range(0, nqubits):
        c.add(gates.RX(i,0))

    result = c()
    print(result.state())
'''
'''except BaseException as e:
    print("An error occurred.")
    print("Error: ", e)
    print("\n Printing callstack ")
    print(traceback.format_exc())'''