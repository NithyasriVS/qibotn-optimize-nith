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
    
def tebd_evol_state_tn_qu(qasm: str, initial_state, mps_opts, tebd_opts, backend="numpy"):
    
    if initial_state is not None:
        nqubits = int(np.log2(len(initial_state)))
        initial_state = init_state_tn(nqubits, initial_state)

    circ_cls = qtn.circuit.CircuitMPS if mps_opts else qtn.circuit.Circuit
    circ_quimb_tebd = circ_cls.from_openqasm2_str(
        qasm, psi0=initial_state, gate_opts=tebd_opts
    )

    ham = tebd_opts['H']
    tebd_obj = circ_quimb_tebd.TEBD(initial_state, ham)
    #tebd_obj = qtn.TEBD(initial_state, ham)
    tebd_obj.split_opts['cutoff'] = 1e-3
    amplitudes = qtn.tebd.evolve(tebd_obj, H=ham, dt=tebd_opts['dt'])

    return amplitudes

def tebd_props_tn_qu(qasm: str, initial_state, mps_opts, tebd_opts, backend="numpy"):

    ham = tebd_opts['H']
    dt = tebd_opts['dt']

    tebd_obj = qtn.TEBD(initial_state, ham)

    entropy = []
    zmag = []
    schmidt_gap = []

    ts = np.linspace(0, 80, 101)
    mz_t_j = []  # z-magnetization
    be_t_b = []  # block entropy
    sg_t_b = []  # schmidt gap

    # range of bonds, and sites
    js = np.arange(0, 44)
    bs = np.arange(1, 44)

    for psit in tebd_obj.at_times(ts, tol=dt):
        mz_j = []
        be_b = []
        sg_b = []
        
        # there is one more site than bond, so start with mag
        #     this also sets the orthog center to 0
        mz_j += [psit.magnetization(0)]
        
        for j in range(1, 44):
            # after which we only need to move it from previous site
            mz_j += [psit.magnetization(j, cur_orthog=j - 1)]
            be_b += [psit.entropy(j, cur_orthog=j)]
            sg_b += [psit.schmidt_gap(j, cur_orthog=j)]
            
        mz_t_j += [mz_j]
        be_t_b += [be_b]
        sg_t_b += [sg_b]
            

        return mz_t_j, be_t_b, sg_t_b