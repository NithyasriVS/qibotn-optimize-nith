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


def dense_vector_tn_qu(qasm: str, initial_state, mps_opts, backend="numpy"):
    """Evaluate circuit in QASM format with Quimb.

    Args:
        qasm (str): QASM program.
        initial_state (list): Initial state in the dense vector form. If ``None`` the default ``|00...0>`` state is used.
        mps_opts (dict): Parameters to tune the gate_opts for mps settings in ``class quimb.tensor.circuit.CircuitMPS``.
        backend (str):  Backend to perform the contraction with, e.g. ``numpy``, ``cupy``, ``jax``. Passed to ``opt_einsum``.

    Returns:
        list: Amplitudes of final state after the simulation of the circuit.
    """

    if initial_state is not None:
        nqubits = int(np.log2(len(initial_state)))
        initial_state = init_state_tn(nqubits, initial_state)

    circ_cls = qtn.circuit.CircuitMPS if mps_opts else qtn.circuit.Circuit
    circ_quimb = circ_cls.from_openqasm2_str(
        qasm, psi0=initial_state, gate_opts=mps_opts
    )

    interim = circ_quimb.psi.full_simplify(seq="DRC")
    amplitudes = interim.to_dense(backend=backend)

    return amplitudes

def tebd_entropy(circuit, initial_state, tebd_opts, backend="numpy"):

    print("ENTERED TEBD_ENTOPY FUNCTION")
    if initial_state is not None:
        nqubits = int(np.log2(len(initial_state)))
        initial_state = init_state_tn(nqubits, initial_state)
    

    ham = circuit.hamiltonian
    numqubits = circuit.nqubits
    tebd = qtn.TEBD(initial_state, ham)

    initial_state = np.zeros(2 ** numqubits) / np.sqrt(2 ** numqubits)

    start = tebd_opts["start"]
    stop = tebd_opts["stop"]
    dt = tebd_opts["dt"]
    
    ts = np.arange(start, stop, dt)
    for psit in tebd.at_times(ts, tol=1e-3):
    
        be_b = []
        for j in range(1, numqubits):

            be_b += [psit.entropy(j, cur_orthog=j)]
        
        be_t_b += [be_b]
        
    return be_t_b

def tebd_zmag(circuit, initial_state, tebd_opts, backend="numpy"):

    if initial_state is not None:
        nqubits = int(np.log2(len(initial_state)))
        initial_state = init_state_tn(nqubits, initial_state)
    
    
    initial_state = np.ones(nqubits, dtype=int)

    ham = circuit.hamiltonian
    numqubits = circuit.nqubits
    tebd = qtn.TEBD(initial_state, ham)

    start = tebd_opts["start"]
    stop = tebd_opts["stop"]
    dt = tebd_opts["dt"]
    
    ts = np.arange(start, stop, dt)
    for psit in tebd.at_times(ts, tol=1e-3):
        
        mz_j = []
        mz_j += [psit.magnetization(0)]
    
        for j in range(1, numqubits):
            mz_j += [psit.magnetization(j, cur_orthog=j - 1)]
        
        mz_t_j += [mz_j]
    
    return mz_t_j
        
def tebd_sgap(circuit, initial_state, tebd_opts, backend="numpy"):

    if initial_state is not None:
        nqubits = int(np.log2(len(initial_state)))
        initial_state = init_state_tn(nqubits, initial_state)

    
    initial_state = np.ones(nqubits, dtype=int)

    ham = circuit.hamiltonian
    numqubits = circuit.nqubits
    tebd = qtn.TEBD(initial_state, ham)

    start = tebd_opts["start"]
    stop = tebd_opts["stop"]
    dt = tebd_opts["dt"]
    
    ts = np.arange(start, stop, dt)
    for psit in tebd.at_times(ts, tol=1e-3):
    
        sg_b = []
        for j in range(1, numqubits):

            sg_b += [psit.schmidt_gap(j, cur_orthog=j)]
        
        sg_t_b += [sg_b]
        
    return sg_t_b