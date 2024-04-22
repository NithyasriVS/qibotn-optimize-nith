from qibo import hamiltonians
from qibo.hamiltonians import SymbolicHamiltonian
import quimb.tensor as qtn
import numpy as np

# input layer

nqubits = 6
dt = 1e-4

ham = hamiltonians.XXZ(nqubits=nqubits, dense=False)
circuit = ham.circuit(dt=dt)

# input layer processing

ham_terms = ham.terms

terms = []
i=0
for t in ham_terms:
    terms.append(t.matrix)
    i=i+1

# splitting into commuting parts

H_odd = []
H_even = []
j=0
while j < len(terms):
    if j % 2 == 0:
        H_even.append(terms[j]*terms[j+1])
    else:
        H_odd.append(terms[j]*terms[j+1])
        j+=1

print(H_odd)
print(H_even)

# exponentiation

for delta in range(0, 1, dt):
    for term in H_odd:
        evol_odd = np.exp(-1*np.imag*delta*H_odd)

for delta in range(0, 1, dt):
    for term in H_even:
        evol_even = np.exp(-1*np.imag*delta*H_even)

final_evol = evol_odd*evol_even

print(final_evol)