import numpy as np
from qibo import hamiltonians

def load_vrp(filename):
    with open(filename) as fh:
    
        data = fh.read()
        lines = data.splitlines()

    dim = int(lines[0])

    distance_matrix = list(map(float, " ".join(lines[1:]).split()))
    distance_matrix = [distance_matrix[i:i + dim] for i in range(0, len(distance_matrix), dim)]

    return dim, distance_matrix

def construct_qubo_no_constraints(dimension, distance_matrix):
    n = len(distance_matrix)

    Q = np.zeros((n*n, n*n))
    distance_matrix = np.array(distance_matrix)

    for i in range(n):
        for j in range(n):
            if i != j:
                Q[i, j] = distance_matrix[i, j]

    return Q

dim, dist = load_vrp('tiny50.dat')
print(dim)

dist = np.matrix(dist)

print(construct_qubo_no_constraints(dim, dist))

hamiltonian = hamiltonians.Hamiltonian(nqubits=2^dim*2^dim,matrix=dist)
print(hamiltonian)