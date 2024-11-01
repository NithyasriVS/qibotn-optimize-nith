import qibo
from qibo import models, optimizers, Circuit, hamiltonians, gates
from qibo.symbols import X, Y, Z
from qibo.optimizers import optimize
import numpy as np
#import qibotn.eval as eval
#from qibo.models.utils import vqe_loss

nqubits = 4
computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": False,
    "NCCL_enabled": False,
    "expectation_enabled": False
}

'''qibo.set_backend(backend="qibotn", platform="cutensornet", runcard=computation_settings)
#qibo.set_backend(backend="qibojit")
problem_hamiltonian = hamiltonians.XXZ(nqubits)

circuit = Circuit(nqubits)
for i in range(0, nqubits):
    circuit.add(gates.H(i))

init_state = circuit().state()

initial_parameters = 0.01 * np.random.random(nqubits)
vqe = models.VQE(circuit, problem_hamiltonian)

i_s = eval.dense_vector_tn(circuit)
vqe.minimize(initial_state= i_s)

loss_func = vqe_loss

loss = lambda p, c, h: problem_hamiltonian.backend.to_numpy(loss_func(p, c, h))
result, parameters, extra = optimizers.optimize(loss, init_state, args=(circuit, problem_hamiltonian), backend=problem_hamiltonian.backend)
'''



circuit = models.Circuit(2)
circuit.add(gates.RY(0, theta=0))
circuit.add(gates.RY(1, theta=0))

hamiltonian = hamiltonians.XXZ(2)
vqe = models.VQE(circuit, hamiltonian)

initial_parameters = np.random.random(2)
vqe.minimize(initial_parameters)

print(vqe.circuit.get_parameters(), type(vqe.circuit.get_parameters()))