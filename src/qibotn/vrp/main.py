"""Vehicle Routing Problem"""

import numpy as np
import argparse
from qubo_utils import binary2spin, spin2QiboHamiltonian

'''from vrp import (
    hamiltonian_vrp,
    qubo_vrp,
    qubo_vrp_penalty
)'''

def load_problem(filename):
    """Load vrp problem from a file

    The file format is compatible with the one used in QAPLIB without considering Flow

    """

    with open(filename) as fh:
        computed_distances = []
        instance_size = int(fh.readline())
        #computed_distances = [float(instance_size) for instance_size in fh.read().split()]
        for l in fh:
            computed_distances_row = [float(x) for x in l.split()]
            computed_distances.append(computed_distances_row)
    
    return computed_distances, instance_size

def build_qubo(distance_matrix, ncust):
    
    lin_qubo = {}
    quad_qubo = {}

    def find_ind(i,j): return i * ncust + j

    for i in range(ncust):
        for j in range(ncust):
            if i != j: # AVOID i to i (seof loops)
                var_index = find_ind(i, j)
                if var_index not in lin_qubo:
                    lin_qubo[var_index] = 0  # Initialize if not already present
                lin_qubo[var_index] += distance_matrix[i][j]

    penalty= 100
    for i in range(ncust):
        # Each point must be exited exactly once
        for j in range(ncust):
            if i != j:
                for k in range(ncust):
                    if k != j and k != i:
                        var1, var2 = find_ind(i, j), find_ind(i, k)
                        if var1 == var2:
                            if var1 not in lin_qubo:
                                lin_qubo[var1] = 0
                            lin_qubo[var1] += penalty
                        else:
                            if (var1, var2) not in quad_qubo:
                                quad_qubo[(var1, var2)] = 0
                            quad_qubo[(var1, var2)] += penalty

        # Each point must be entered exactly once
        for j in range(ncust):
            if i != j:
                for k in range(ncust):
                    if k != i and k != j:
                        var1, var2 = find_ind(j, i), find_ind(k, i)
                        if var1 == var2:
                            if var1 not in lin_qubo:
                                lin_qubo[var1] = 0
                            lin_qubo[var1] += penalty
                        else:
                            if (var1, var2) not in quad_qubo:
                                quad_qubo[(var1, var2)] = 0
                            quad_qubo[(var1, var2)] += penalty

    # Start and end at the depot (point 0)
    for j in range(1, ncust):
        start_var = find_ind(0, j)
        end_var = find_ind(j, 0)
        if start_var not in lin_qubo:
            lin_qubo[start_var] = 0
        lin_qubo[start_var] += penalty
        if end_var not in lin_qubo:
            lin_qubo[end_var] = 0
        lin_qubo[end_var] += penalty

    return lin_qubo, quad_qubo

def build_ham():

    dm, size = load_problem("src/qibotn/vrp/data.txt")
    linear, quadratic = build_qubo(dm, size)

    h, J, _ = binary2spin(linear, quadratic)
    h = {k: -v for k, v in h.items()}
    J = {k: -v for k, v in J.items()}

    ham = spin2QiboHamiltonian(h, J)

    return ham

'''def qubo_vrp(D, p):
    m = len(D)
    qubo = np.zeros((m), dtype=np.float32)
    
    offset = p * 2 * m
    for x in range(0,m):
            qubo[x] = (D[x])

    linear = {i: qubo[i] for i in range(qubo.shape[0])}
    #quadratic = {
    #    (i): qubo[i] for j in range(qubo.shape[1]) for i in range(qubo.shape[0]) if i > j
    #}
    quadratic = {i: qubo[i] for i in range(qubo.shape[0])}

    return linear, quadratic, offset


def hamiltonian_vrp(D, penalty):
    linear, quadratic, offset = qubo_vrp(D, penalty)

    h, J, _ = binary2spin(linear, quadratic)
    h = {k: -v for k, v in h.items()}
    J = {k: -v for k, v in J.items()}

    hamiltonian = spin2QiboHamiltonian(h, J)

    return hamiltonian

'''
def main():

    ham = build_ham()
    print(ham, type(ham))

if __name__ == "__main__":
    main()