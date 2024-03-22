import numpy as np
from qibo import models, gates, hamiltonians

nqubits = 6
nlayers  = 4

# Create variational circuit
circuit = models.Circuit(nqubits)
for l in range(nlayers):
    circuit.add((gates.RY(q, theta=0) for q in range(nqubits)))
    circuit.add((gates.CZ(q, q+1) for q in range(0, nqubits-1, 2)))
    circuit.add((gates.RY(q, theta=0) for q in range(nqubits)))
    circuit.add((gates.CZ(q, q+1) for q in range(1, nqubits-2, 2)))
    circuit.add(gates.CZ(0, nqubits-1))
circuit.add((gates.RY(q, theta=0) for q in range(nqubits)))

# Create XXZ Hamiltonian
hamiltonian = hamiltonians.XXZ(nqubits=nqubits)
# Create VQE model
vqe = models.VQE(circuit, hamiltonian)

'''# Optimize starting from a random guess for the variational parameters
initial_parameters = np.random.uniform(0, 2*np.pi,
                                        2*nqubits*nlayers + nqubits)
best, params, extra = vqe.minimize(initial_parameters, method='BFGS', compile=False)'''

c = vqe.circuit 
h = vqe.hamiltonian


