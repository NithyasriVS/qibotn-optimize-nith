import numpy as np
import math
import itertools as iter
import networkx as nx
from qibo import Circuit, models, gates, hamiltonians

cust_coords = []
demands = []
start = (0, 0)

def load_vrp(datafile):
    '''Load VRP problem from a file'''
    with open('belgium-road-km-n50-k10.txt', 'r') as f:
        vrp_data = f.readlines()

    for data, l in enumerate(vrp_data):
        
        if l.startswith("DIMENSION"):
            ncust = int(l.split(":")[1].strip())
        elif l.startswith("EDGE_WEIGHT_TYPE"):
            wt_type = l.split(":")[1].strip()
        
        if l.startswith("NODE_COORD_SECTION"):
            lat_long = l.split()
            cust_coords.append((float(lat_long[1]), float(lat_long[2])))
            #cust_label = lat_long[3]
        
        if l.startswith("DEMAND_SECTION"):
            demand = l.split()
            demands.append(int(demand[1]))
    
    return ncust, wt_type, cust_coords, demands

def distance_matrix(cust_coords, edge_wt_type):
    
    n = len(cust_coords)
    distance_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if edge_wt_type == "EUC_2D":
                distance_matrix = np.linalg.norm(cust_coords[:, np.newaxis] - cust_coords, axis=2)

                
            elif edge_wt_type == "GEO":
                R = 6371
                lat1, lon1 = math.radians(cust_coords[i][0]), math.radians(cust_coords[i][1])
                lat2, lon2 = math.radians(cust_coords[j][0]), math.radians(cust_coords[j][1])
                distance_matrix[i][j] = R * math.acos(
                    math.sin(lat1) * math.sin(lat2) +
                    math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)
                )
            else:
                raise ValueError(f"Unsupported EDGE_WEIGHT_TYPE: {edge_wt_type}")

    return distance_matrix

def data2graph():
    G = nx.Graph()

def qubo_vrp():

    # qubo og is sum(wij . xij) - weights, binary 

    # typical constraints
    # no subtours (basically same customer visited without going from depot)
    # a customer is visited exactly once
    # must start and end at depot

    # need to give "penalties" for each constraints if violated
    
    # other constraints: time? (finish and come back to depot in t amount of time?)

    # focus on time as metric - latency - target optimz goal
    print("OG QUBO, then apply the constraints as penalties")

def qubo2hamiltonian():
    print("Write function here")

def vrp_ansatz():
    print("Return the ansatz circuit which is an input for vqe")

def vrp_vqe():
    print("Call vqe with this hamiltonian")

# Is this kind of a design the correct approach
# Metrics where do they fit into this? (Throughput, Runtime) - is it after the VQE is run, we check these?