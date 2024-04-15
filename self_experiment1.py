import qibo
from qibo import hamiltonians, gates, models
from qibo import Circuit

# Step 1) Cast a hamiltonian as circuit using TD
ham = hamiltonians.XXZ(nqubits=5, dense=False)
circuit = ham.circuit(dt=1e-2)

def handle_unitary(circuit):
    return circuit.unitary()

matrix_of_combined_local_unitaries = handle_unitary(circuit)
print(matrix_of_combined_local_unitaries)

 
'''dec = circuit.decompose(0)
print(circuit.summary)
print(circuit.draw)
print(dec)

# Step 2) Extraction of hamiltonian from circuit
# 15apr
print(circuit.unitary()) # experiment 2 -> converts to 2^n x 2^n matrix
# Method 1: OpenQASM
# Challenge: Unitary is not supported by OpenQASM
# 15apr [IMPORTANT COMMENT]: this error is not coming from qibo circuits.py but directly from OpenQASM
print(circuit.to_qasm())
# Method 2: Manual extraction
# Challenge: Not able to extract as a matrix
def extract_local_unitaries(circuit):
    lu = []
    for gate in circuit.gates_of_type(qibo.gates.Unitary):
        lu = gate.matrix
    return lu
print(extract_local_unitaries(circuit))'''
