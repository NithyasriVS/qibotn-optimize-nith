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

entropy = callbacks.EntanglementEntropy([0], compute_spectrum=True)

ham = hamiltonians.TFIM(nqubits=5, dense=False)
c = ham.circuit(dt=1e-3)

c.add(gates.CallbackGate(entropy))

evolve = models.StateEvolution(ham, dt=1e-3)
print(evolve)
nqubits = 5
initial_state = np.ones(2 ** nqubits) / np.sqrt(2 ** nqubits)
evolve = models.StateEvolution(ham, dt=1e-3, callbacks=[entropy])
print(evolve.callbacks[0].spectrum)
final_state = evolve(final_time=1, start_time=0, initial_state=initial_state)

print(entropy.spectrum)





