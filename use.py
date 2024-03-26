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

nqubits = 5
dt = 1e-3
initial_state = np.ones(nqubits, dtype=int)

observable = callbacks.EntanglementEntropy(compute_spectrum=True)

ham = hamiltonians.TFIM(nqubits=5, dense=False)
circuit = ham.circuit(dt=dt)
#circuit.add(gates.CallbackGate(observable))

#final_state = circuit()

evolve = models.StateEvolution(ham, dt=1e-3, callbacks=[observable])
final_state = evolve(final_time=1, initial_state=initial_state)

print(observable.spectrum)






'''nqubits = 5
initial_state = np.ones(nqubits, dtype=int)

observable = callbacks.EntanglementEntropy([0])

ham = hamiltonians.TFIM(nqubits=5, dense=False)
circuit = ham.circuit(dt=1e-2)

circuit.add(gates.CallbackGate(observable))

final_state = circuit()


#evolve = models.StateEvolution(ham, dt=1e-3, callbacks=[observable])
#final_state = evolve(final_time=1, initial_state=initial_state)

#print(final_state)
print(observable[0])'''

