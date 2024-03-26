from qibo import hamiltonians, models
import numpy as np

nqubits = 5

# Define TFIM model as a non-dense ``SymbolicHamiltonian``
ham = hamiltonians.TFIM(nqubits=5, dense=False)
# This object can be used to create the circuit that
# implements a single Trotter time step ``dt``
circuit = ham.circuit(dt=1e-2)

initial_state = np.ones(2 ** nqubits) / np.sqrt(2 ** nqubits)
# Define the evolution model
evolve = models.StateEvolution(ham, dt=1e-3)
# Evolve for total time T=1
final_state = evolve(final_time=1, initial_state=initial_state)

print(final_state)