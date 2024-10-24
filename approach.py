import qibo
from qibo import hamiltonians, Circuit, gates, models
import numpy as np
from qibo.symbols import Z,X

# Approach 1

# user'll give follwoing as inputs in the runcard in the actual workflow
nqubits=4
p = 5
circuit = Circuit(nqubits)
for i in range(0,nqubits):
 circuit.add(gates.H(i))

ham_cost = hamiltonians.SymbolicHamiltonian(Z(0) * Z(1))
ham_mixer = hamiltonians.SymbolicHamiltonian(X(0)*X(1))

initial_parameters = 0.01 * np.random.uniform(0,1,4)

# QAOA starts

qaoa_model = models.QAOA(hamiltonian=ham_cost, mixer=ham_mixer)
best_energy, final_parameters, extra = qaoa_model.minimize(initial_parameters, method="BFGS")

# extract final parameter

gammas = final_parameters[::2] # every even
betas = final_parameters[1::2] # every odd

# build a circuit with alternating layers of ham cost with gamma_i and ham mixer with beta_i

hc_arr = []
hm_arr = []
qubit_indices = list(range(nqubits))

# Exponential hamiltonians into Unitary gates that can be applied on Circuit
if ham_mixer is not None:
    for g in gammas:
        u_ham_cost = ham_cost.exp(g)
        hc_arr.append(gates.Unitary(u_ham_cost, *qubit_indices))
    for b in betas:
        u_ham_mixer = ham_mixer.exp(b)
        hm_arr.append(gates.Unitary(u_ham_mixer, *qubit_indices))

# Construct Alternating Layers
for circ_depth in range(0, p):
    for uhc in hc_arr:
        circuit.add(uhc)
    for uhm in hm_arr:
        circuit.add(uhm)

print("Approach 1: ", circuit.draw())

# return this circuit to qibotn eval to convert to TN
# output will be the expectation value of TN


# Approach 2: 
# Using VQE (Considering QAOA as a special case of VQE)
# Why? Because QAOA doesn't expose the circuit but VQE has ansatz in its design

# user'll give follwoing as inputs in the runcard in the actual workflow
nqubits=2
circuit = Circuit(nqubits)
for i in range(0,nqubits):
 circuit.add(gates.RZ(i, theta=0))

ham_cost = hamiltonians.XXZ(2)
ham_mixer = hamiltonians.XXZ(2)

initial_parameters = 0.01 * np.random.uniform(0,1,2)
final_parameters = 0.03 * np.random.uniform(0,1,2)

vqe_model = models.VQE(circuit, ham_cost)
#loop which feeds back into minimize from qibotn side 
#iteratively
best_energy, final_parameters = vqe_model.minimize(initial_parameters)
gamma_circ = vqe_model.circuit
print("Approach 2: Initial Circuit\n", gamma_circ.draw())

qaoa_model = models.VQE(gamma_circ, ham_mixer)
qaoa_model.minimize(final_parameters)
final_circ = qaoa_model.circuit
print("Approach 2: Final Circuit\n", final_circ.draw())

# -> return the circuit to eval -> return expectation value
# Approach 3:

# Extract hamiltonian terms and turn them in tensors 
# Prepare uniform superposition circuit and apply the ham tensors on them
'''
nqubits=4
p = 5
circuit = Circuit(nqubits)
for i in range(0,nqubits):
 circuit.add(gates.H(i))

ham_cost = hamiltonians.SymbolicHamiltonian(Z(0) * Z(1))
ham_mixer = hamiltonians.SymbolicHamiltonian(X(0)*X(1))

initial_parameters = 0.01 * np.random.uniform(0,1,4)

# QAOA starts

qaoa_model = models.QAOA(hamiltonian=ham_cost, mixer=ham_mixer)
best_energy, final_parameters, extra = qaoa_model.minimize(initial_parameters, method="BFGS")

# extract final parameter

gammas = final_parameters[::2] # every even
betas = final_parameters[1::2] # every odd

hc_arr = []
hm_arr = []

# Exponential hamiltonians into Unitary gates that can be applied on Circuit
if ham_mixer is not None:
    for g in gammas:
        u_ham_cost = ham_cost.exp(g)
        hc_arr.append(u_ham_cost)
                
    for b in betas:
        u_ham_mixer = ham_mixer.exp(b)
        hm_arr.append(u_ham_mixer)

#print("Terms ",hc_arr, "Type: ",type(hc_arr), "Element of List ",type(hc_arr[0]))

# Hams -> Einsums
terms_dict = {}
i = 0
hclist = ham_cost.terms
for tc in hclist:
    terms_dict.update({None: tc.matrix})
    i = i + 1

i = 0
hmlist = ham_mixer.terms    
for tm in hmlist:
    terms_dict.update({None: tm.matrix})
    i = i + 1'''
'''
import quimb
ham_cost = hamiltonians.SymbolicHamiltonian(Z(0) * Z(1))
ham_mixer = hamiltonians.SymbolicHamiltonian(X(0)*X(1))

terms = ham_cost.matrix  
num_qubits = nqubits

# Initialize a list for edges
edges = []

# Create edges based on Hamiltonian terms
for coefficient, term in terms:
    # Here, we assume term is a string like 'Z0Z1', meaning an edge between qubit 0 and qubit 1
    qubits = [int(q) for q in term if q.isdigit()]  # Extract qubit indices
    if len(qubits) == 2:  # Only consider 2-qubit interactions for edges
        edges.append((qubits[0], qubits[1], coefficient))  # (source, target, weight)

# Now create a Quimb graph
graph = quimb.Graph()
for source, target, weight in edges:
    graph.add_edge(source, target, weight=weight)

terms = {(i, j): 1 for i, j in graph.edges}

import quimb.tensor as qtn
p = 2
gammas = quimb.randn(p)
betas = quimb.randn(p)
circ_ex = qtn.circ_qaoa(terms, p, gammas, betas)

def energy(x):
    p = len(x) // 2
    gammas = x[:p]
    betas = x[p:]
    circ = qtn.circ_qaoa(terms, p, gammas, betas)

    ZZ = quimb.pauli('Z') & quimb.pauli('Z')

    ens = [
        circ.local_expectation(weight * ZZ, edge, optimize='greedy', backend="jax")
        for edge, weight in terms.items()
    ]
    
    print(sum(ens).real)
'''

# Approach 4: Quimb

import quimb
import quimb.tensor as qtn

qasm_str = final_circ.to_qasm()
circ_cls = qtn.circuit.CircuitMPS

circ_quimb = circ_cls.from_openqasm2_str(
        qasm_str
    )

gammas = quimb.randn(p)
betas = quimb.randn(p)
qc = qtn.circ_qaoa(circ_quimb, p, gammas, betas)









