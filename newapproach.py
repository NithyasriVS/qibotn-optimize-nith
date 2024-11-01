import qibo
from qibo import hamiltonians, Circuit, gates, models
import numpy as np
from qibo import optimizers
from qibo.optimizers import optimize
from qibo.result import QuantumState
#import qibotn.eval as eval
import eval

nlayers = 5 # will come from runcard
# hamiltonian names will be there in runcard, we need to contruct the ham accordingly

computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": False,
    "NCCL_enabled": False,
    "expectation_enabled": False
}

qibo.set_backend(backend="qibotn", platform="cutensornet", runcard=computation_settings)

def vqe_loss_tn(params, circuit, hamiltonian):
        circuit.set_parameters(params)
        
        # 1) direct
        result = eval.dense_vector_tn(circuit,"complex64") 
        # if this done directly, there's compatibility error when loss is being used in minimize()

        # hamiltonian.backend.eval.dense_vector_tn(circuit,"complex64") 
        # result = circuit.backend.eval.dense_vector_tn(circuit,"complex64") # if this is done circuit.backend is not possible
        final_state = result.state()
        #result = eval.dense_vector_tn(circuit,"complex64").flatten()
        
        final_state = QuantumState(result)
        # return hamiltonian.expectation(final_state) # in original vqe_loss()
        #return circuit.expectation(final_state)
        return final_state

        '''2) use exact syntax used by qibo but instead of execute_circuit(), do eval.dense_vector_tn()
             if this done error is "CuTensornet cannot process Initial State"
           3) swap out hamiltonian.backend to circuit.backend 
        
            but actually, our guy is execute_circuit()'''
        

nqubits = 3

circuit = Circuit(nqubits)
for i in range(0, nqubits):
    circuit.add(gates.RX(i, 0))

hamiltonian = hamiltonians.XXZ(nqubits)

class VQE_tn:

    def __init__(self, circuit, hamiltonian):
        
        self.circuit = circuit
        self.hamiltonian = hamiltonian
    
    def minimize_tn(initial_parameters, initial_state, loss_func, method):
        
        for i in range(0, nlayers):
            if loss_func is None:
                loss = vqe_loss_tn(initial_parameters, circuit, hamiltonian)
            
            if method == "cma":
                dtype = circuit.backend.np.float64
                loss = (
                    (lambda p, c, h: loss_func(p, c, h).item())
                    if str(dtype) == "torch.float64"
                    else (lambda p, c, h: dtype(loss_func(p, c, h)))
                )
            elif method != "sgd":
                loss = lambda p, c, h: circuit.backend.to_numpy(loss_func(p, c, h))
            result, parameters, extra = optimize(
                loss,
                initial_state,
                args=(circuit, hamiltonian),
                method=method
                backend=circuit.backend
            )
        circuit.set_parameters(parameters)
        return result, parameters, extra

initial_parameters = 0.01 * np.random.random(nqubits)

vqe_model = VQE_tn(circuit, hamiltonian)
# loop this for nlayers
vqe_model.minimize_tn(initial_parameters, loss_func=vqe_loss_tn(initial_parameters, circuit, hamiltonian))

params = vqe_model.circuit.get_parameters()
state = np.array(params).flatten()
print(QuantumState(state.flatten()))






import qibo
from qibo import hamiltonians, Circuit, gates, models
import numpy as np

nqubits = 2

omputation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": False,
    "NCCL_enabled": False,
    "expectation_enabled": False
}

qibo.set_backend(backend="qibotn", platform="cutensornet", runcard=computation_settings)

hamiltonian = hamiltonians.XXZ(nqubits)
circuit = Circuit(nqubits)
for i in range(0, nqubits):
    circuit.add(gates.RX(i, 0))

initial_parameters = 0.01 * np.random.random(nqubits)
vqe_model = models.VQE(circuit, hamiltonian)
vqe_model.minimize(initial_parameters)

c = vqe_model.circuit # CHECK WHAT TYPE OF CIRCUIT OBJECT THIS IS
result = c()
print(result.state())











