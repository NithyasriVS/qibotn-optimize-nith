from qubo_utils import binary2spin, spin2QiboHamiltonian
import qibo
from qibo import Circuit, models, gates
import numpy as np

ncust = 4

distance_matrix= [
    [0.0, 9.849096, 8.29975427, 10.34143689, 5.27563503],
    [9.849096, 0.0, 2.81998316, 0.71700279, 5.80897728],
    [8.29975427, 2.81998316, 0.0, 2.81583664, 5.78378993],
    [10.34143689, 0.71700279, 2.81583664, 0.0, 6.47844441],
    [5.27563503, 5.80897728, 5.78378993, 6.47844441, 0.0]
]

'''distance_matrix = [
    [0.0, 1.0, 2.0, 3.0],
    [1.0, 0.0, 4.0, 5.0],
    [2.0, 6.0, 0.0, 1.0],
    [3.0, 4.0, 2.0, 0.0] 
]'''

def build_qubo(distance_matrix, ncust):
    lin_qubo = {}
    quad_qubo = {}

    def find_ind(i, j, ncust): 
        return i * ncust + j  # Flatten 2D to 1D

    # Constructing the QUBO terms
    for i in range(ncust):
        for j in range(ncust):
            if i != j:  # Skip self-loops
                var_index = find_ind(i, j, ncust)
                
                if var_index not in lin_qubo:
                    lin_qubo[var_index] = 0
                lin_qubo[var_index] += distance_matrix[i][j]

    penalty = 100  # Penalty for violating constraints

    # Add constraints (each point must be entered and exited exactly once)
    for i in range(ncust):
        for j in range(ncust):
            if i != j:
                for k in range(ncust):
                    if k != j and k != i:
                        var1, var2 = find_ind(i, j, ncust), find_ind(i, k, ncust)
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
                        var1, var2 = find_ind(j, i, ncust), find_ind(k, i, ncust)
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
        start_var = find_ind(0, j, ncust)
        end_var = find_ind(j, 0, ncust)
        if start_var not in lin_qubo:
            lin_qubo[start_var] = 0
        lin_qubo[start_var] += penalty
        if end_var not in lin_qubo:
            lin_qubo[end_var] = 0
        lin_qubo[end_var] += penalty

    return lin_qubo, quad_qubo

'''def build_qubo_for_multiple_vehicles(distance_matrix, ncust, nvehicle):
    lin_qubo_n = {}
    quad_qubo_n = {}

    # Flatten to 1D
    def find_ind(i, j, ncust, nvehicle): 
        return i * ncust + j  # Map 2D index (i, j) to a 1D index

    return lin_qubo_n, quad_qubo_n
'''

'''
def build_nqubo(distance_matrix, ncust, nvehicle):
    lin_nqubo = {}
    quad_nqubo = {}

    def find_ind(i, j, ncust, nvehicle):
        return i * ncust + + j * nvehicle #custmer, vehicle

    penalty = 100  # Penalty for violating constraints
    
    # 1. Distance costs: for each pair of customers (i, j), add the corresponding distance as a linear term.
    for i in range(ncust):
        for j in range(ncust):
            if i != j:  # Skip self-loops
                var_index = find_ind(i, j, ncust, nvehicle)
                if var_index not in lin_qubo:
                    lin_qubo[var_index] = 0
                lin_qubo[var_index] += distance_matrix[i][j]  # Add distance cost to the linear term

    # 2. Constraints to ensure each customer is visited exactly once:
    for i in range(ncust):
        for j in range(ncust):
            if i != j:
                for k in range(ncust):
                    if k != j and k != i:
                        var1, var2 = find_ind(i, j, ncust, nvehicle), find_ind(i, k, ncust, nvehicle)
                        if var1 == var2:  # If the customer i is assigned to multiple vehicles
                            if var1 not in lin_qubo:
                                lin_qubo[var1] = 0
                            lin_qubo[var1] += penalty
                        else:
                            if (var1, var2) not in quad_qubo:
                                quad_qubo[(var1, var2)] = 0
                            quad_qubo[(var1, var2)] += penalty

    # 3. Each customer must be assigned to exactly one vehicle:
    for i in range(ncust):
        for j in range(nvehicle):
            for k in range(nvehicle):
                if j != k:
                    var1, var2 = find_ind(i, j, ncust, nvehicle), find_ind(i, k, ncust, nvehicle)
                    if var1 == var2:  # If two vehicles are assigned to the same customer
                        if var1 not in lin_qubo:
                            lin_qubo[var1] = 0
                        lin_qubo[var1] += penalty
                    else:
                        if (var1, var2) not in quad_qubo:
                            quad_qubo[(var1, var2)] = 0
                        quad_qubo[(var1, var2)] += penalty

    # 4. Ensure each vehicle has a valid route:
    for j in range(nvehicle):
        # Each vehicle should have at least one customer
        for i in range(ncust):
            var = find_ind(i, j, ncust, nvehicle)
            if var not in lin_qubo:
                lin_qubo[var] = 0
            lin_qubo[var] += penalty

    # 5. Start and end at the depot (point 0):
    for j in range(1, ncust):
        start_var = find_ind(0, j, ncust, nvehicle)  # Customer j assigned to vehicle at start
        end_var = find_ind(j, 0, ncust, nvehicle)    # Customer j assigned to vehicle at end
        if start_var not in lin_qubo:
            lin_qubo[start_var] = 0
        lin_qubo[start_var] += penalty  # Enforce start at depot
        if end_var not in lin_qubo:
            lin_qubo[end_var] = 0
        lin_qubo[end_var] += penalty  # Enforce end at depot

    return lin_nqubo, quad_nqubo'''

# Generate the QUBO from the distance matrix
lin_qubo, quad_qubo = build_qubo(distance_matrix, ncust)


#print("QUBO Linear Terms:", lin_qubo)
#print("QUBO Quadratic Terms:", quad_qubo)

# Covert QUBO to an ising model first

''' Working example: Only 1 vehicle'''
h, J, _ = binary2spin(lin_qubo, quad_qubo)
h = {k: -v for k, v in h.items()} # bias
J = {k: -v for k, v in J.items()} # interaction

ham = spin2QiboHamiltonian(h, J, dense=False)

print(ham, type(ham), ham.nqubits)
ham_qub = ham.nqubits


nqubits = 15
c = Circuit(nqubits)
for i in range(0, nqubits):
    c.add(gates.RX(i,0))

test_vqe = models.VQE(c, ham)
initial_parameters=np.random.uniform(0, 2 * np.pi, ham_qub)

print(test_vqe.minimize(initial_parameters))

measurements = test_vqe.circuit.execute(nshots=10)

print(measurements)


# Let's try more complex case

#lin_nqubo, quad_nqubo = build_nqubo(distance_matrix, ncust, nvehicle=3)
'''
h, J, _ = binary2spin(lin_nqubo, quad_nqubo)
h = {k: -v for k, v in h.items()} # bias
J = {k: -v for k, v in J.items()} # interaction

ham = spin2QiboHamiltonian(h, J, dense=False)

print(ham, type(ham), ham.nqubits)
ham_qub = ham.nqubits

nqubits = ham_qub
c = Circuit(nqubits)
for i in range(0, nqubits):
    c.add(gates.RX(i,0))

test_vqe = models.VQE(c, ham)
initial_parameters=np.random.uniform(0, 2 * np.pi, ham_qub)

print(test_vqe.minimize(initial_parameters))

measurements = test_vqe.circuit.execute(nshots=10)

print(measurements)
'''