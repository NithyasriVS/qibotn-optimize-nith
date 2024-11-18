import qibo
from qibo import models, hamiltonians, Circuit, gates
import numpy as np
from qibo.result import QuantumState

import qibotn.eval as eval

nqubits = 4

c = Circuit(nqubits)
for i in range(0, nqubits):
    c.add(gates.RX(i,0))

VQE_execute = {"hamiltoninan": "XXZ", "initial_parameters": 0.01 * np.random.random(nqubits)}
print("vqe is: ",VQE_execute)
print("yes but first", VQE_execute is True, " yes but second", VQE_execute == True)
ham = VQE_execute["hamiltoninan"]
init_params = VQE_execute["initial_parameters"]

computation_settings = {
            "MPI_enabled": False,
            "MPS_enabled": False,
            "NCCL_enabled": False,
            "expectation_enabled": False
}

qibo.set_backend(backend="qibotn", platform="cutensornet", runcard=computation_settings)
    
#if VQE_execute is True:
if VQE_execute:
        print("vqe execute is true")
        if ham == "XXZ":
            hamiltonian = hamiltonians.XXZ(nqubits)
        if ham == "MaxCut":
            hamiltonian = hamiltonians.MaxCut(nqubits)
        if ham == "X":
            hamiltonian = hamiltonians.X(nqubits)
        if ham == "Y":
            hamiltonian = hamiltonians.Y(nqubits)
        if ham == "Z":
            hamiltonian = hamiltonians.Z(nqubits)
        if ham == "TFIM":
            hamiltonian = hamiltonians.TFIM(nqubits)
        if ham == "custom":
            # need to find a way to construct a hamiltonian from a string given?
            print("Not supported as of now")
vqe = models.VQE(c, hamiltonian)

'''
need own to_numpy for qibotn?

def to_numpy(self, x):
        if self.is_sparse(x):
            return x.toarray()
        return x
'''

def vqe_loss_qibotn(params, circuit, hamiltonian):

    circuit.set_parameters(params)
    result = hamiltonian.backend.execute_circuit(circuit)
    #final_state = result.state(numpy=True)
    final_state = result.state()
    final_state = final_state.get()
    dtype = np.float64
    return hamiltonian.expectation(final_state)



    
print("Final Paramters of VQE = ", vqe.minimize(init_params, loss_func=vqe_loss_qibotn(init_params, c, hamiltonian), method="cma"))
final_circ = vqe.circuit

    
print("Final Circ = ", final_circ.draw())
state = eval.dense_vector_tn(final_circ, "complex64")
print("Qibojit execute ", final_circ().state())
print("Qibotn eval function output ",QuantumState(state.flatten()))