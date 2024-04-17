import numpy as np
from qibo import Circuit, gates, hamiltonians
import qibo

# Below shows how to set the computation_settings
# Note that for MPS_enabled and expectation_enabled parameters the accepted inputs are boolean or a dictionary with the format shown below.
# If computation_settings is not specified, the default setting is used in which all booleans will be False.
# This will trigger the dense vector computation of the tensornet.

dt = 1e-2
nqubits = 5

computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": False,
    "NCCL_enabled": False,
    "expectation_enabled": False,
    "TEBD_enabled" : {"dt":dt, "hamiltonian":"TFIM"}
}

# Possible list of hamiltonians
# TFIM: transverse field ising model
# XXZ: heisenberg 
# NIX: non-interacting pauli x
# NIY: non-interacting pauli y
# NIZ: non-interacting pauli z
# MC: maxcut

# Raise an NotImplemented error if not from this list

qibo.set_backend(backend="qibotn", platform="qutensornet", runcard=computation_settings)


# Construct the circuit
ham = hamiltonians.XXZ(nqubits=nqubits)
circuit = ham.circuit(dt=dt)

# Execute the circuit and obtain the final state
result = circuit()

print(result.state())
