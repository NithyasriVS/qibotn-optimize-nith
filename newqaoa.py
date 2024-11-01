
import qibo
from qibo import hamiltonians, Circuit, gates, models
from qibo.symbols import Z

z0=Z(0)
z1=Z(1)
hamiltonian = hamiltonians.SymbolicHamiltonian(z0+z1)
qaoa = models.QAOA(hamiltonian)

accelerators = None



chc = qaoa.hamiltonian.circuit(1e-2, accelerators) # Generates the cost Hamiltonian circuit
mhc = qaoa.mixer.circuit(1e-2, accelerators)       # Generates the mixer Hamiltonian circuit

concatenated_circuit = chc + mhc
#print(concatenated_circuit.draw())

concatenated_circuit