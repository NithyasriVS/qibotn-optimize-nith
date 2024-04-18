import qibo
from qibo import hamiltonians, gates, models
from qibo import Circuit
from qibo.quantum_info import pauli_basis, comp_basis_to_pauli
from qibo.hamiltonians import SymbolicHamiltonian as sh
import sympy

'''print(circuit.summary())
print(ham.terms)
for t in ham.terms:
    print("Matrix:",t.matrix)
#print("Ham terms",sh._get_symbol_matrix(self,ham.terms))
print(ham.matrix)
def handle_unitary(circuit):
    return circuit.unitary()
matrix_of_combined_local_unitaries = handle_unitary(circuit)
print(matrix_of_combined_local_unitaries)'''
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


# Step 1) Cast a hamiltonian as circuit using TD
ham = hamiltonians.XXZ(nqubits=5, dense=False)
circuit = ham.circuit(dt=1e-2)

# print(circuit.unitary()) - gives effective 2^n x 2^n matrix of all gates in circ combined

print("Circuit Summary:",circuit.summary())
print("\nLet's now print the terms in the hamiltonian\n")

list_of_terms = ham.terms # using symbolic representation of gates in qibo

i=0
for t in list_of_terms:
    print("Term ",i," :",t.matrix)
    i=i+1

'''import quimb.tensor as qtn
import numpy as np

nqubits=5

dims = tuple(np.ones(nqubits, dtype=int))
             
initial_state = qtn.tensor_1

tebd_object = qtn.TEBD(initial_state, ham.matrix)

print(tebd_object)'''

print("Print as an effective 2^n x 2^n matrix: ",ham.matrix) # symbolic rep effective matrix 

# one potential issue here is how to do reverse ham.circuit to circuit.hamiltonian to get the ham 
# in another python file where tebd is gonna happen like circuit.hamiltonian

# one workaround/solution:
'''in the runcard, the user can specify the name of the hamiltonian. This will however have one
limitation that there can't be custom hams. User will be restricted to pre-defined symbolic hams in
qibo eg. TFIM, XXZ, MaxCut, Non-interacting Pauli X, Y, Z which must be set  with dense=False'''

