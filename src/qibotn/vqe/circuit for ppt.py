from qibo import Circuit, gates

nqubits = 5
nlayers = 1


circuit = Circuit(nqubits)
for _ in range(nlayers):
        circuit.add(gates.RY(q, theta=0) for q in range(nqubits))
        circuit.add(gates.RZ(q, theta=0) for q in range(nqubits))
        circuit.add(gates.CZ(q, q + 1) for q in range(0, nqubits - 1, 2))
        circuit.add(gates.RY(q, theta=0) for q in range(nqubits))
        circuit.add(gates.RZ(q, theta=0) for q in range(nqubits))
        circuit.add(gates.CZ(q, q + 1) for q in range(1, nqubits - 2, 2))
        circuit.add(gates.CZ(0, nqubits - 1))
circuit.add(gates.RY(q, theta=0) for q in range(nqubits))

print(circuit.draw())


import numpy as np

from qibo import Circuit, gates
from qibo.hamiltonians import XXZ
from qibo.models import VQE

# create circuit ansatz for two qubits
circuit = Circuit(2)
circuit.add(gates.RY(0, theta=0))
# create XXZ Hamiltonian for two qubits
hamiltonian = XXZ(2)
# create VQE model for the circuit and Hamiltonian
vqe = VQE(circuit, hamiltonian)
# optimize using random initial variational parameters
initial_parameters = np.random.uniform(0, 2, 1)
vqe.minimize(initial_parameters)

