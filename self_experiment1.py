import qibo
from qibo import hamiltonians, gates

# Step 1) Cast a hamiltonian as circuit using TD
ham = hamiltonians.XXZ(nqubits=5, dense=False)
circuit = ham.circuit(dt=1e-2)

# Step 2) Extraction of hamiltonian from circuit

# Method 1: OpenQASM
# Challenge: Unitary is not supported by OpenQASM
print(circuit.to_qasm())

# Method 2: Manual extraction
# Challenge: Not able to extract as a matrix

def extract_local_unitaries(circuit):
    lu = []
    for gate in circuit.gates_of_type(qibo.gates.Unitary):
        lu = gate.matrix
    return lu
print(extract_local_unitaries(circuit))
