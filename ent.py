from qibo import models, gates, callbacks, hamiltonians
import numpy as np

entropy = callbacks.EntanglementEntropy([0], compute_spectrum=True)

ham = hamiltonians.TFIM(nqubits=5, dense=False)
c = ham.circuit(dt=1e-3)

c.add(gates.CallbackGate(entropy))

evolve = models.StateEvolution(ham, dt=1e-3)
nqubits = 5
initial_state = np.ones(2 ** nqubits) / np.sqrt(2 ** nqubits)
evolve = models.StateEvolution(ham, dt=1e-3)
final_state = evolve(final_time=1, initial_state=initial_state)

print(entropy[:])
