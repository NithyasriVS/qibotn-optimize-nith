import quimb.tensor as qtn
from qibo import hamiltonians
from qibo.hamiltonians import SymbolicHamiltonian

#qibo_ham = hamiltonians.XXZ(nqubits=5)
#circuit = qibo_ham.circuit(dt=1e-4)

#ham_terms = qibo_ham.terms

'''terms = []
i=0
for t in ham_terms:
    terms.append(t.matrix)
    i=i+1'''

L = 5
binary = '00000'
psi0 = qtn.MPS_computational_state(binary)

ham = qtn.ham_1d_heis(L)

qtn.TEBD(ham, psi0)