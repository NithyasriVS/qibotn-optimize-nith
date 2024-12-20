import numpy as np
from qibo import hamiltonians, models, Circuit, gates
import networkx as nx

coords = []

def load_vrp(filename):
    """Load qap problem from a file
        
       The file format is compatible with the one used in TSPLIB
    """
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
    """Given a list of coordinates, calculates the 2 dimensional Eucledian pairwise distance between all pairs 
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


'''def vrp_graph(coords, distance_matrix):
    vrpG = nx.Graph
 
    for i in coords:
        for j in coords:
                vrpG = nx.add_edges(i, j, weight=distance_matrix[i][j])
    return vrpG'''

#def vrp_hamiltonian(graph):

c = load_vrp("smallerdataset.txt")
dm = distance_matrix(c)
#vg = vrp_graph(c, dm)

x = [0,1,1,0,1,0,0,1,1,1]
qubo = sum(x*w for x,w in zip(x, dm))

print(dm, type(dm))










        




