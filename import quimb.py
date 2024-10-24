import quimb 
import networkx as nx
import quimb.tensor as qtn
import qibo
from qibo import hamiltonians, Circuit, gates, models
import numpy as np


import networkx as nx
import re

def qasm_to_random_regular_graph(qasm_string):
    # Step 1: Parse the QASM string
    qubit_count = 0

    # Extract the number of qubits from the QASM string
    qasm_lines = qasm_string.splitlines()
    for line in qasm_lines:
        line = line.strip()
        if line.startswith('qreg'):
            # Extract the number of qubits from qreg
            match = re.search(r'qreg\s+(q\[\d+\])', line)
            if match:
                qubit_count = int(re.search(r'\d+', match.group(0)).group(0))

        # Only consider single-qubit gates (RX, RY, RZ)
        elif 'RX' in line or 'RY' in line or 'RZ' in line:
            continue  # Do nothing, as these gates do not create edges

    # Step 2: Define the graph parameters
    n = qubit_count  # number of nodes (qubits)
    if n == 0:
        raise ValueError("No qubits found in the QASM string.")
    
    # For a regular graph, degree must be less than the number of qubits
    degree = 1  # Set degree to 1 for simplicity (can be adjusted based on your needs)
    
    # Ensure degree is even and appropriate for a regular graph
    if degree >= n:
        raise ValueError(f"Cannot create a regular graph with {n} nodes and degree {degree}.")

    # Step 3: Create a random regular graph
    random_graph = nx.random_regular_graph(degree, n)

    return random_graph


nqubits=2
circuit = Circuit(nqubits)
for i in range(0,nqubits):
 circuit.add(gates.RZ(i, theta=0))

ham_cost = hamiltonians.XXZ(2)
ham_mixer = hamiltonians.XXZ(2)

initial_parameters = 0.01 * np.random.uniform(0,1,2)
final_parameters = 0.03 * np.random.uniform(0,1,2)

vqe_model = models.VQE(circuit, ham_cost)
vqe_model.minimize(initial_parameters)
gamma_circ = vqe_model.circuit
print("Approach 2: Initial Circuit\n", gamma_circ.draw())

#qaoa_model = models.VQE(gamma_circ, ham_mixer)
#qaoa_model.minimize(final_parameters)
#final_circ = qaoa_model.circuit
#print("Approach 2: Final Circuit\n", final_circ.draw())
qasm_str = gamma_circ.to_qasm()


graph = qasm_to_random_regular_graph(qasm_str)

print(graph)

