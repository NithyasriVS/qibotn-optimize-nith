import traceback
import qibo
from qibo.result import QuantumState
from qibo import Circuit, gates, hamiltonians, models
from qibo.symbols import Z
import numpy as np


def vqe_loss_qibotn(params, circuit, hamiltonian):
    '''circuit.set_parameters(params)
    print("Hamiltonian Backend: ",hamiltonian.backend, type(hamiltonian.backend)) # qibotn (cutensornet) - what it should be? CuTensorNet?
    result = hamiltonian.backend.execute_circuit(circuit)
    print("result and its type: ", result, type(result))
    final_state = result.state() # cannot calculate Hamiltonian expectation value for  state of type cupy.ndarray
    #final_state = QuantumState(result.state()) # cannot calculate Hamiltonian expectation value for state of type <class 'qibo.result.QuantumState'>
    #final_state = result.state().get() # numpy float object is not callable
    return hamiltonian.expectation(final_state)'''

    circuit.set_parameters(params)
    print("Hamiltonian Backend: ",hamiltonian.backend, type(hamiltonian.backend))
    result = hamiltonian.backend.execute_circuit(circuit)
    print("result and its type: ", result, type(result))
    #result = result.state()
    final_state = result.state(numpy=True)
    return hamiltonian.expectation(final_state)

try:
    computation_settings = {
            "MPI_enabled": False,
            "MPS_enabled": False,
            "NCCL_enabled": False,
            "expectation_enabled": False,
            "VQE_execute": True
    }
    '''computation_settings = {
            "MPI_enabled": False,
            "MPS_enabled": False,
            "NCCL_enabled": False,
            "expectation_enabled": False
    }'''

    qibo.set_backend(backend="qibotn", platform="cutensornet", runcard=computation_settings)

    nqubits = 2
    c = Circuit(nqubits)
    for i in range(0, nqubits):
        c.add(gates.RX(i,0))

    hamiltonian = hamiltonians.XXZ(nqubits)
    #hamiltonian = hamiltonians.SymbolicHamiltonian(sum([Z(0), Z(1)]))
    initial_parameters = 0.01 * np.random.random(nqubits)

    vqe = models.VQE(c, hamiltonian)
    #vqe.minimize(initial_parameters)
    vqe.minimize(initial_parameters, loss_func=vqe_loss_qibotn(initial_parameters, c, hamiltonian))

    c=vqe.circuit
    print(c.draw)

    result = c()
    print(result.state())

except BaseException as e:
    print("An error occurred.")
    print("Error: ", e)
    print("\n Printing callstack ")
    print(traceback.format_exc())