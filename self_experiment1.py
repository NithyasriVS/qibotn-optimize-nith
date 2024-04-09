# A self experiment on how to cast H as qibo circuit and extract unitaries for next steps in process

import qibo
from qibo import hamiltonians, gates

# Casting of a hamiltonian as a circuit using TD
ham = hamiltonians.XXZ(nqubits=5, dense=False)
circuit = ham.circuit(dt=1e-2)

# Method 1: OpenQASM
# Challenge 1: Unitary is not supported by OpenQASM

#print(circuit.to_qasm())

# Method 2: Extracting Unitaries manually
# Challenge 2: We can extract the unitaries but we need as matrices

def extract_local_unitaries(circuit):
    """Extract local unitaries from a Qibo circuit."""
    local_unitaries = []
    for gate in circuit.gates_of_type(qibo.gates.Unitary):
        local_unitaries = gate.matrix
    return local_unitaries

print(extract_local_unitaries(circuit))




