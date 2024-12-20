import numpy as np
import math
import itertools as iter
import networkx as nx
from qibo import Circuit, models, gates, hamiltonians

cust_coords = []
distance_matrix = []
start = (0, 0)
element = []
edge_weight_section = True
node_coord_section = True

k = 10

with open('belgium-road-km-n50-k10.txt', 'r') as f:
        vrp_data = f.readlines()

# Define an empty list to hold the latitudes and longitudes
coordinates = []


# Flag to indicate whether we are in the NODE_COORD_SECTION
in_node_coord_section = False
in_edge_weight_section = True

for line in vrp_data:
    line = line.strip()

    if "NODE_COORD_SECTION" in line:
        in_node_coord_section = True
        if line.startswith("EDGE_WEIGHT_SECTION"):
            break
        continue
    
    if in_node_coord_section and line:
        parts = line.split()
        if len(parts) >= 3:
            latitude = parts[1]
            longitude = parts[2]
            coordinates.append((latitude, longitude))
    #print(coordinates)

    if line.startswith("EDGE_WEIGHT_SECTION"):
        
        pass
        in_edge_weight_section = True
        if line.startswith("DEMAND_SECTION"): break
        if line.strip() == "":   break
        element = line.split()
        if element:  
            distance_matrix.append(list(map(float, element)))

'''for data, l in enumerate(vrp_data):
        
        if l.startswith("DIMENSION"):
            ncust = int(l.split(":")[1].strip())
            print(ncust)
        
        if l.startswith("NODE_COORD_SECTION"):
            l.strip().split()
            if l == "NODE_COORD_SECTION": pass

            for i in range(len(l)):
            
                latitude = float(l[i][0])  
                longitude = float(l[i][1])
            cust_coords.append(latitude, longitude)
        
            print(cust_coords)
        elif l.strip() == "EDGE_WEIGHT_SECTION":
            edge_weight_section = True
        elif edge_weight_section:
            if l.strip() == "":  
                break
            
            row = [float(x) for x in l.strip().split() if x.replace('.', '', 1).isdigit()]
            if row:
                distance_matrix.append(row)
        
        #print(distance_matrix)
        
#if l.strip() == "DEMAND_SECTION":
           '''  
              