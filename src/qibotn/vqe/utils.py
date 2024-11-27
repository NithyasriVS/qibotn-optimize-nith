import numpy as np

# Loss function for Variational Quantum Eigensolver
def vqe_loss_qibotn(p, c, h):
        def loss_return(p, c, h):
                c.set_parameters(p)
                result = h.backend.execute_circuit(c)
                final_state = result.state()
                final_state = final_state.get()
                return h.expectation(final_state)
        return loss_return

# Extract and Rerun the data for the Vehicle Routing Problem
def extract_vrp_data(f):
        
        with open(f, 'r') as file:
                ls = file.readlines()
        
        dist = []

        cust_coords = []
        demands = []

        depot_coords = (0, 0) # start with oth depot

        for data, l in enumerate(ls):
                if l.startswith("DIMENSION"):
                        ncust = int(l.split(":")[1].strip())
                if l.startswith("CAPACITY"):
                        cap = int(l.split(":")[1].strip())
                # Extract the coordinates
                if l.startswith("NODE_COORD_SECTION"):
                        begin_coord = data+1
                        for j in range(begin_coord, begin_coord+ncust):
                                info = ls[j].split()
                                cust_coords.append((int(info[1]), int(info[2])))
                        # Extract the customer demands
                        if l.startswith("DEMAND_SECTION"):
                                begin_demands = data+1
                                for j in range(begin_demands, begin_demands+ncust):
                                        info = ls[j].split()
                                        demands.append(int(info[1]))

                        if l.startswith("DEPOT_SECTION"):
                                depot = cust_coords[0]
                        if l.startswith("COMMENT") and "No of trucks" in l:
                                # Extract the number from the line
                                nvehicles = int(l.split("No of trucks:")[1].split(",")[0].strip())
                                break
                
        # Distance Matrix for QUBO 
        dist= np.zeros((ncust+1, ncust+1))  # Including depot
        for i in range(ncust+1):
                for j in range(i+1, ncust+1):
                        if i == 0 or j == 0:  # Distance from depot to customer
                                distance = np.linalg.norm(np.array(depot) - np.array(cust_coords[j - 1]))
                        else:  # Distance between two customers
                                distance = np.linalg.norm(np.array(cust_coords[i - 1]) - np.array(cust_coords[j - 1]))
                        dist[i][j] = distance
                        dist[j][i] = distance
        
        return dist, ncust, nvehicles, cap, demands

# Construct the QUBO based on the Distance Matrix

def construct_qubo(dist_matrix, ncust, nvehicle, vehicle_cap, cust_demands):
        print("need to write")

def qubo2ham():
        print("need to write")


                        


