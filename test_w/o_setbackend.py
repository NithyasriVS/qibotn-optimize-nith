#import eval_qu as eq
import quimb

import numpy as np
import quimb.tensor as qtn


def init_state_tn(nqubits, init_state_sv):
    """Create a matrix product state directly from a dense vector.

    Args:
        nqubits (int): Total number of qubits in the circuit.
        init_state_sv (list): Initial state in the dense vector form.

    Returns:
        list: Matrix product state representation of the dense vector.
    """

    dims = tuple(2 * np.ones(nqubits, dtype=int))

    return qtn.tensor_1d.MatrixProductState.from_dense(init_state_sv, dims)

nqubits = 32
zeros = '0' * ((nqubits - 2) // 3)
binary = zeros + '1' + zeros + '1' + zeros
initial_state =  qtn.MPS_computational_state(binary)
#initial_state = init_state_tn(nqubits, binary)

computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": {
        "qr_method": False,
        "svd_method": {
            "partition": "UV",
            "abs_cutoff": 1e-12,
        },
    },
    "TEBD_enabled": {
        "H": qtn.ham_1d_heis(32),
        "dt": 1e-3
    },
    "NCCL_enabled": False,
    "expectation_enabled": False,
}

tebd_opts = computation_settings['TEBD_enabled']

#if computation_settings['TEBD_enabled'] == True:
H = tebd_opts['H']
dt = tebd_opts['dt']

#if computation_settings['MPS_enabled'] == True:
mps_opts = {
        "qr_method": False,
        "svd_method": {
            "partition": "UV",
            "abs_cutoff": 1e-12,
        }
    }

def main(qasm: str, initial_state, mps_opts, tebd_opts):
    
    print("[DEBUGGING STATEMENT] Let's find the TEBD entropy")

    '''if initial_state is not None:
        nqubits = int(np.log2(32))
        initial_state = init_state_tn(nqubits, initial_state)'''

    circ_cls = qtn.circuit.CircuitMPS if mps_opts else qtn.circuit.Circuit
    circ_quimb = circ_cls.from_openqasm2_str(
        qasm, psi0=initial_state, gate_opts=mps_opts
    )
    H = tebd_opts['H']
    tebd = qtn.TEBD(circ_quimb, H)
    
    ts = np.linspace(0, 80, 101)
    
    for psit in tebd.at_times(ts, tol=1e-3):
    
        be_b = []
    
        for j in range(1, 44):

            be_b += [psit.entropy(j, cur_orthog=j)]
        
        be_t_b += [be_b]
        
    return be_t_b

if __name__ == "__main__":
    main(initial_state, initial_state, mps_opts, tebd_opts)