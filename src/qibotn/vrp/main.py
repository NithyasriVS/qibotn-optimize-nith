"""Vehicle Routing Problem"""

import numpy as np
import argparse
from qubo_utils import binary2spin, spin2QiboHamiltonian

'''from vrp import (
    hamiltonian_vrp,
    qubo_vrp,
    qubo_vrp_penalty
)'''

def load_vrp(filename):
    """Load vrp problem from a file

    The file format is compatible with the one used in QAPLIB without considering Flow

    """

    with open(filename) as fh:
        instance_size = int(fh.readline())

        d = [float(instance_size) for instance_size in fh.read().split()]

    return d

def qubo_vrp(D, p):
    m = len(D)
    qubo = np.zeros((m**2, m**2), dtype=np.float32)
    
    offset = p * 2 * m
    for x in range(m):
        for y in range(m):
            # flatten into 1D
            qubo_element = x*m + y
            qubo[qubo_element,qubo_element] = D[x][y]

    linear = {i: qubo[i, i] for i in range(qubo.shape[0])}
    quadratic = {
        (i, j): qubo[i, j] for j in range(qubo.shape[1]) for i in range(qubo.shape[0]) if i > j
    }

    return linear, quadratic, offset

        
    return qubo

def hamiltonian_vrp(D, penalty):
    linear, quadratic, offset = qubo_vrp(D, penalty)

    h, J, _ = binary2spin(linear, quadratic)
    h = {k: -v for k, v in h.items()}
    J = {k: -v for k, v in J.items()}

    hamiltonian = spin2QiboHamiltonian(h, J)

    return hamiltonian


def main(filename):
    print(f"Load distance matrices from {filename} and make a QUBO")
    D = load_vrp(filename)

    linear, quadratic, offset = qubo_vrp((D), penalty=0)

    print("Construct a hamiltonian directly from distance matrix")
    ham = hamiltonian_vrp((D), dense=False)

    print("done.")

if __name__ == "__main__":
    main("tiny0502.dat")

