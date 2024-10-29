import qibo
from qibo import models, optimizers, Circuit, hamiltonians
from qibo.symbols import X, Y, Z
from qibo.optimizers import optimize
import numpy as np

nqubits = 4
computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": False,
    "NCCL_enabled": False,
    "expectation_enabled": False
}

qibo.set_backend(backend="qibotn", platform="qutensornet", runcard=computation_settings)

#problem_hamiltonian = hamiltonians.XXZ(nqubits)
problem_hamiltonian = hamiltonians.SymbolicHamiltonian(sum([X(0) * X(1), Y(0) * Y(1), 0.5 * Z(0) * Z(1)]))

print(problem_hamiltonian.backend)

init_state = problem_hamiltonian.backend.plus_state(nqubits)
print(init_state, type(init_state))
params = 0.01 * np.random.random(nqubits)

qaoa = models.QAOA(problem_hamiltonian, mixer=None)

# iterative
#params = optimize here

qaoa.set_parameters(params)

final_state = qaoa.execute(initial_state=init_state)
print(qaoa.hamiltonian.circuit(dt=0.1)) # return the circuit to qibotn
# and it sends back dense vector which becomes init_state for execute and 
# final_state for loss fn for next iteration



#loss = problem_hamiltonian.expectation(final_state)
# qibo.optimizers.cmaes(loss, initial_parameters)


