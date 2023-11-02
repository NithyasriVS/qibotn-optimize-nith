import copy
import os
from timeit import default_timer as timer

import config
import numpy as np
import pytest
import qibo
from qibo.models import QFT


def create_init_state(nqubits):
    init_state = np.random.random(2**nqubits) + \
        1j * np.random.random(2**nqubits)
    init_state = init_state / np.sqrt((np.abs(init_state) ** 2).sum())
    return init_state


def qibo_qft(nqubits, init_state, swaps):
    circ_qibo = QFT(nqubits, swaps)
    state_vec = np.array(circ_qibo(init_state))
    return circ_qibo, state_vec


def time(func):
    start = timer()
    res = func()
    end = timer()
    time = end - start
    return time, res


@pytest.mark.parametrize("nqubits, tolerance",
                         [(1, 1e-6), (2, 1e-6), (5, 1e-3), (10, 1e-3)])
def test_eval(nqubits: int, tolerance: float):
    # hack quimb to use the correct number of processes
    # TODO: remove completely, or at least delegate to the backend
    # implementation
    os.environ["QUIMB_NUM_PROCS"] = str(os.cpu_count())
    import qibotn.quimb

    init_state = create_init_state(nqubits=nqubits)
    init_state_tn = copy.deepcopy(init_state)

    # Test qibo
    qibo.set_backend(backend=config.qibo.backend,
                     platform=config.qibo.platform)
    qibo_time, (qibo_circ, result_sv) = time(
        lambda: qibo_qft(nqubits, init_state, swaps=True)
    )

    # Convert to qasm for other backends
    qasm_circ = qibo_circ.to_qasm()

    # Test quimb
    quimb_time, result_tn = time(
        lambda: qibotn.quimb.eval(
            qasm_circ, init_state_tn, backend=config.quimb.backend
        )
    )

    assert 1e-2 * qibo_time < quimb_time < 1e2 * qibo_time
    assert np.allclose(result_sv, result_tn,
                       atol=tolerance), "Resulting dense vectors do not match"
