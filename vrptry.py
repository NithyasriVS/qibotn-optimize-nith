import numpy as np
import itertools as iter
import networkx as nx
from qibo import Circuit, models, gates, hamiltonians


filename = "vrp_dataset32.txt"
cust_coords = []
demands = []
depot = (0, 0)
    
with open(filename, 'r') as file:
    ls = file.readlines()

for data, l in enumerate(ls):
    if l.startswith("DIMENSION"):
        ncust = int(l.split(":")[1].strip())
    if l.startswith("CAPACITY"):
        cap = int(l.split(":")[1].strip())
        
    if l.startswith("NODE_COORD_SECTION"):
        begin_coord = data + 1
        for j in range(begin_coord, begin_coord + ncust):
            info = ls[j].split()
            cust_coords.append((int(info[1]), int(info[2])))
        
        if l.startswith("DEMAND_SECTION"):
            begin_demands = data + 1
            for j in range(begin_demands, begin_demands + ncust):
                info = ls[j].split()
                demands.append(int(info[1]))

        if l.startswith("DEPOT_SECTION"):
            depot = cust_coords[0]  # start 1st cust is the depot itself
        if l.startswith("COMMENT") and "No of trucks" in l:
            
            nvehicles = int(l.split("No of trucks:")[1].split(",")[0].strip())
            break

G = nx.Graph()

for i, (c, d) in enumerate(zip(cust_coords, demands)):
        node_id = i + 1
        G.add_node(node_id, pos=c, demand=d)

G.add_node(0, pos=(0, 0), demand=0)

def distance(coord1, coord2):
        return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

# Edges b/w customers
for i in range(ncust):
        for j in range(i + 1, ncust):
            dist = distance(cust_coords[i], cust_coords[j])
            G.add_edge(i + 1, j + 1, weight=dist)
    
# Edges from depot to each customer
for i in range(ncust):
        dist = distance(depot, cust_coords[i])
        G.add_edge(0, i + 1, weight=dist)

print(G)

def create_qubo_hamiltonian(G):
    terms = []
    
    # Nodes represent customers (excluding depot)
    nodes = list(G.nodes)[1:]  # Skip depot (node 0)
    
    # Loop through each pair of nodes (i, j) and get the interaction (distance)
    for i in range(1, len(nodes) + 1):
        for j in range(i + 1, len(nodes) + 1):
            # Get distance (weight of edge)
            distance = G[i][j]['weight']
            
            # Add quadratic interaction term between x_i and x_j (QUBO formulation)
            terms.append((distance, i - 1, j - 1))  # i - 1, j - 1 to map to 0-indexed binary variables
    
    # Return the Hamiltonian (it needs to be ising generally)
    return hamiltonians.Hamiltonian(terms)

print(create_qubo_hamiltonian(G))














