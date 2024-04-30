import eval_qu as eval
import qibo
from qibo import hamiltonians

dt = 1e-4
nqubits = 5

''''computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": False,
    "NCCL_enabled": False,
    "expectation_enabled": False,
    "TEBD_enabled" : {"dt":dt, "hamiltonian":"XXZ", "initial_state":"10101", "tot_time":1}
}

qibo.set_backend(backend="qibotn", platform="qutensornet", runcard=computation_settings)'''

initial_state = '10101'
tebd_opts = {"dt":1e-4, "hamiltonian": "XXZ", "initial_state": "10101", "tot_time":1}
nqubits = 5

ham = hamiltonians.XXZ(nqubits=nqubits, dense=False)
circuit = ham.circuit(dt=dt)

print(eval.tebd_tn_qu(circuit, tebd_opts, initial_state, nqubits))

