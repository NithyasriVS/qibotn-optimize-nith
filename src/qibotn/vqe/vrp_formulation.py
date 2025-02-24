from vrp_utils import binary2spin, spin2QiboHamiltonian, load_vrp, distance_matrix
import qibo
from qibo import Circuit, models, gates
import numpy as np
from vqe_tn import run_vqe
from vrp_utils import extract_data
from utils import plot_result, calc_final_measurement

#filename = "data1.txt" # 5 vehicles
#filename = "data2.txt" # 4 vehicles
#filename = "data3.txt" # 3 vehicles
filename = "data4.txt" # 6 vehicles
#filename = "data5.txt" #  10 vehicles

ncust, dm = extract_data(filename)


# Take actual data from file later, test with toy matrix first
'''
ncust = 5
distance_matrix= [
    [0.0, 9.849096, 8.29975427, 10.34143689, 5.27563503],
    [9.849096, 0.0, 2.81998316, 0.71700279, 5.80897728],
    [8.29975427, 2.81998316, 0.0, 2.81583664, 5.78378993],
    [10.34143689, 0.71700279, 2.81583664, 0.0, 6.47844441],
    [5.27563503, 5.80897728, 5.78378993, 6.47844441, 0.0]
]

distance_matrix = dm
'''
def build_qubo(distance_mat, ncust):
    lin_qubo = {}
    quad_qubo = {}

    def find_ind(i, j, ncust): 
        return i * ncust + j  # Flatten 2D to 1D

    # Construct QUBO terms
    for i in range(ncust):
        for j in range(ncust):
            if i != j:  # No self-loops
                var_index = find_ind(i, j, ncust)
                
                if var_index not in lin_qubo:
                    lin_qubo[var_index] = 0
                lin_qubo[var_index] += distance_mat[i][j]

    penalty = 100  # Penalty for violating constraints

    # Add constraints 
    # Flow contstraint: Enter AND Exit a customer location and only once
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

        # Each customer location entered exactly once
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

    # Always start and end at depot
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

# Generate the QUBO from the distance matrix
lin_qubo, quad_qubo = build_qubo(dm, ncust)

# Covert QUBO to an ising model first
''' Working example: 1 vehicle'''
h, J = binary2spin(lin_qubo, quad_qubo)
h = {k: -v for k, v in h.items()} # bias
J = {k: -v for k, v in J.items()} # interaction

ham = spin2QiboHamiltonian(h, J, dense=False)

print("Number of Qubits: ",ham.nqubits,"\n")
nqubits = ham.nqubits

'''
c = Circuit(nqubits)
for i in range(0, nqubits):
    c.add(gates.RX(i,0))'''

# Using BOOSTVQE library to construct a hardware efficient ansatz
from boostvqe.ansatze import hdw_efficient

c = hdw_efficient(nqubits=nqubits, nlayers=1)

# Entanglement missing
# Hardware Efficient Ansatz (Generic) - nlayers, nqubits are inputs - tune nlayers

    # Check qibojit annealing - design of ansatz

'''Hardware Efficient Ansatz'''
'''numlayers = 2
for _ in range(0,numlayers):
    for i in range(0,nqubits):
        c.add(gates.RY(i,0))
    c.add(gates.CNOT(0, nqubits-1))'''
initial_parameters=np.random.uniform(0, 2 * np.pi, nqubits*5)

# .state() try to set qibotn backend before that or use qibotn .state() - > this part look into 
circ_temp = c
circ_temp.set_parameters(initial_parameters)
initial_state = circ_temp().state()

vqe_circuit = run_vqe(c, ham, initial_parameters)
result = vqe_circuit()
#print(result.state())

final_state = result.state()

#not needed measurements = vqe_circuit(nshots=10)
measurements = vqe_circuit(nshots=1000)

print("Measurements: ", measurements)

bitstr = str(measurements)
print("Final measurement output: ",calc_final_measurement(bitstr))

#output = measurements.state()
#print("Final measurement result: ",output,"\n")

plot_result()

'''print("Prob",measurements.probabilities())

p = measurements.probabilities()
p_max_n = np.argmax(p)
max_prob = p[p_max_n]
output = measurements.state()
output = output[p_max_n]
print("Final measurement result: ",output,"\n")
'''
'''
freq = measurements.frequencies(binary=True)
max_freq = max(freq, key=freq.get)
print("Most common result: ",max_freq,"\n")
'''


print("Expectation Value of Initial State: ", ham.expectation(initial_state),"\n")
print("Expectation Value of Final State: ", ham.expectation(final_state))

#print(measurements)

'''CPU Qibojit
test_vqe = models.VQE(c, ham)
initial_parameters=np.random.uniform(0, 2 * np.pi, nqubits)

print(test_vqe.minimize(initial_parameters))

measurements = test_vqe.circuit.execute(nshots=10)

print(measurements)
'''
# frequency highest = result