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
print("Terms",terms)

# splitting into commuting parts

H_odd = []
H_even = []
j=0
# 0 odd 1 even 2 odd 3 even 
while j < len(terms):
    if j % 2 == 0:
        H_odd.append(terms[j]*terms[j+1])
    else:
        H_even.append(terms[j]*terms[j+1])
        j+=1

print("Hodd",H_odd)
print("Heven",H_even)

'''# exponentiation

for delta in range(0, 1, dt):
    for term in H_odd:
        evol_odd = np.exp(-1*np.imag*delta*H_odd)

for delta in range(0, 1, dt):
    for term in H_even:
        evol_even = np.exp(-1*np.imag*delta*H_even)

U_tebd1 = evol_odd*evol_even'''

