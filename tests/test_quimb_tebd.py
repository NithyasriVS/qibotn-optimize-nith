import copy
import os

import config
import numpy as np
import pytest
import qibo

def create_init_state(nqubits):
    init_state = np.random.random(2**nqubits) + 1j * np.random.random(2**nqubits)
    init_state = init_state / np.sqrt((np.abs(init_state) ** 2).sum())
    return init_state

@pytest.mark.parametrize(
    "nqubits, tolerance, is_mps",
    [(1, 1e-6, True), (2, 1e-6, False), (5, 1e-3, True), (10, 1e-3, False)],
)
def test_eval(nqubits: int, tolerance: float, is_mps: bool):
    """Evaluate circuit with Quimb backend.

    Args:
        nqubits (int): Total number of qubits in the system.
        tolerance (float): Maximum limit allowed for difference in results
        is_mps (bool): True if state is MPS and False for tensor network structure
    """
    # hack quimb to use the correct number of processes
    # TODO: remove completely, or at least delegate to the backend
    # implementation
    os.environ["QUIMB_NUM_PROCS"] = str(os.cpu_count())
    import qibotn.eval_qu

    init_state = create_init_state(nqubits=nqubits)
    init_state_tn = copy.deepcopy(init_state)

    # Test qibo
    qibo.set_backend(backend=config.qibo.backend, platform=config.qibo.platform)
