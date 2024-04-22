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

def tebd_tn_qu(hamiltonian_terms, dt, nqubits):

    for i in range(0,nqubits): # initial state will always be n zeros
        binary = ''+'0'
    psi0 = qtn.MPS_computational_state(binary)


    #H = qtn.ham_1d_heis(L)
    H = qtn.LocalHam1D(nqubits, H2=hamiltonian_terms)

    tebd = qtn.TEBD(psi0, H)

    dt=dt
    tot = 1
    ts = np.arange(0, tot, dt)

    interim = next(tebd.at_times(ts,tol=1e-3))

    amplitudes = interim.to_dense()
    print(amplitudes)
    return amplitudes


    
        




