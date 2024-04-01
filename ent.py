from qibo import models, gates, callbacks, hamiltonians

entropy = callbacks.EntanglementEntropy([0], compute_spectrum=True)

ham = hamiltonians.TFIM(nqubits=5, dense=False)
c = ham.circuit(dt=1e-3)

c.add(gates.CallbackGate(entropy))


final_state = c()
print(entropy[:])

print(entropy.spectrum)
