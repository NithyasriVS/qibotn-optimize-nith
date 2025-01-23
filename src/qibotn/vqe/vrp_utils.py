import numpy as np

def load_vrp(filename):
    """Load vrp problem coordinates from the dataset
    """
    coords = []
    with open(filename,'r') as dataset:
        data = dataset.readlines()
        bool_coord = False
    for d in data:
        d = d.strip()
        if d == "NODE_COORD_SECTION":
            bool_coord = True
            continue
        if d == "DEMAND_SECTION":
            bool_coord = False
            break
        if bool_coord:
            nodes = d.split()
            x = float(nodes[1])
            y = float(nodes[2])
            coords.append((x, y))
    return coords

def distance_matrix(coordinates):
    """Given a list of coordinates, calculates the 2D Eucledian pairwise distance between all pairs 
        of coordinates

        Since a distance matrix is one that's upper triangular and symmetric, these properties are exploited
    """
    ncustomers = len(coordinates)
    dist_matrix = np.zeros((ncustomers,ncustomers))
    for i in range(ncustomers):
        for j in range(i+1, ncustomers):
            euc_2d = np.linalg.norm(np.array(coordinates[i]) - np.array(coordinates[j]))
            dist_matrix[i][j] = euc_2d
            dist_matrix[j][i] = euc_2d
    return dist_matrix

from typing import Dict, Tuple

# Inspired and reused from Qibo QAP Application
def binary2spin(
    linear: Dict[int, float],
    quadratic: Dict[Tuple[int, int], float],
):
    """Convert binary QUBO model to Ising model
    """

    h = {x: 0.5 * w for x, w in linear.items()}

    J = []
    for (x, y), w in quadratic.items():
        J.append(((x, y), 0.25 * w))
        h[x] += 0.25 * w
        h[y] += 0.25 * w
    J = dict(J)

    return h, J

# Inspired and reused from Qibo QAP Application
def spin2QiboHamiltonian(
    h: Dict[int, float],
    J: Dict[Tuple[int, int], float],
    dense: bool = True,
):
    """Convert ising model to qibo Hamiltonian
    """

    from qibo import hamiltonians
    from qibo.symbols import Z

    form = 0
    for k, v in h.items():
        form -= Z(k, commutative=True) * v
    for (k0, k1), v in J.items():
        form -= Z(k0, commutative=True) * Z(k1, commutative=True) * v

    ham = hamiltonians.SymbolicHamiltonian(form)

    if dense:
        return ham.dense
    else:
        return ham