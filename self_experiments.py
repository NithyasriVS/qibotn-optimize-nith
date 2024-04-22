import qibo
from qibo import hamiltonians, gates, models
from qibo import Circuit
from qibo.quantum_info import pauli_basis, comp_basis_to_pauli
from qibo.hamiltonians import SymbolicHamiltonian
import sympy
import qibotn.backends.quimb as qmb



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

dt = 1e-4
nqubits = 5 

computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": False,
    "NCCL_enabled": False,
    "expectation_enabled": False,
    "TEBD_enabled" : {"dt":dt, "hamiltonian":"TFIM"}
}

'''# Step 1) Cast a hamiltonian as circuit using TD
ham = hamiltonians.XXZ(nqubits=nqubits, dense=False)
circuit = ham.circuit(dt=dt)'''

qibo.set_backend(backend="qibotn", platform="qutensornet", runcard=computation_settings)


print(qmb.invoke_tebd())
'''# Execute the circuit and obtain the final state
result = circuit()

print(result.state())'''

# print(circuit.unitary()) - gives effective 2^n x 2^n matrix of all gates in circ combined

'''print("Circuit Summary:",circuit.summary())
print("\nLet's now print the terms in the hamiltonian\n")

list_of_terms = ham.terms # using symbolic representation of gates in qibo

terms_list = []
i=0
for t in list_of_terms:
    terms_list.append(t.matrix)
    print("Term ",i," :",t.matrix)
    i=i+1

print("Type ", type(list_of_terms))

#actual_dict = dict(terms_dict)
print(terms_list)


terms_dict = {}
i=0
for t in list_of_terms:
    terms_dict.update({None: t.matrix})
    i=i+1
print(terms_dict)'''

'''import quimb.tensor as qtn
import numpy as np

nqubits=5

dims = tuple(np.ones(nqubits, dtype=int))
             
initial_state = qtn.tensor_1

tebd_object = qtn.TEBD(initial_state, ham.matrix)

print(tebd_object)'''

#print("Print as an effective 2^n x 2^n matrix: ",ham.matrix) # symbolic rep effective matrix 

# one potential issue here is how to do reverse ham.circuit to circuit.hamiltonian to get the ham 
# in another python file where tebd is gonna happen like circuit.hamiltonian

# one workaround/solution:
'''in the runcard, the user can specify the name of the hamiltonian. This will however have one
limitation that there can't be custom hams. User will be restricted to pre-defined symbolic hams in
qibo eg. TFIM, XXZ, MaxCut, Non-interacting Pauli X, Y, Z which must be set  with dense=False'''


'''i = 0
commute = []

while i < len(list_of_terms):
        if i % 2 != 0:
            commute.append(list_of_terms[i]*list_of_terms[i+1])
        i+=1

print("Internally commuting parts",commute)'''

'''Independent working code:
import quimb.tensor as qtn
import numpy as np

L = 5
binary = '00000'
psi0 = qtn.MPS_computational_state(binary)


#H = qtn.ham_1d_heis(L)
H = qtn.LocalHam1D(L, H2=terms_dict)

print("Quimb ham ",H)

tebd = qtn.TEBD(psi0, H)

dt=1e-4
tot = 1
ts = np.arange(0, tot, dt)

#print(yield from tebd.at_times(ts))

x = next(tebd.at_times(ts,tol=tot))

print(x)

print(x.to_dense())

for psi in tebd.at_times(ts, tol=1e-4):

    print(tebd.at_times(psi))

mz_t_j = []
for psi in tebd.at_times(ts, tol=tot):
    mz_j = []
    mz_j += [psi.magnetization(0)]

    for j in range(1, L):
        # after which we only need to move it from previous site
        mz_j += [psi.magnetization(j, cur_orthog=j - 1)]
    mz_t_j += [mz_j]'''













