import numpy as np
from qibo import Circuit, gates, hamiltonians, models, callbacks
import qibo

computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": False,
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

nqubits = 2
dt = 1e-3
initial_state = np.ones((2,2))

observable = callbacks.EntanglementEntropy()

ham = hamiltonians.TFIM(nqubits=nqubits, dense=False)
circuit = ham.circuit(dt=dt)
circuit.add(gates.CallbackGate(observable))

evolve = models.StateEvolution(ham, dt=1e-3, callbacks=[observable])
final_state = evolve(final_time=1, initial_state=initial_state)

print(final_state)

