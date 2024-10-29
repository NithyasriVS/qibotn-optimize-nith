import qibo
from qibo import hamiltonians, models, gates, Circuit
import numpy as np
import qibotn.eval as eval

def prepare_qaoa_circuit(runcard):

    ham_cost = runcard["Hcost"]
    ham_mixer = runcard["Hmixer"] # optional
    p = runcard["circ_depth"]
    initial_parameters = runcard["init_params"]
    dt = runcard["dt"]
    nqubits = runcard["nqubits"]
    
    # Plus state preparation circuit
    circuit = Circuit(nqubits)
    for i in range(0,nqubits):
        circuit.add(gates.H(i))

    # QAOA starts

    qaoa_model = models.QAOA(hamiltonian=ham_cost, mixer=ham_mixer)
    best_energy, final_parameters, extra = qaoa_model.minimize(initial_parameters, method="BFGS")

    # extract final parameter

    gammas = final_parameters[::2] # every even
    betas = final_parameters[1::2] # every odd

    # build a circuit with alternating layers of ham cost with gamma_i and ham mixer with beta_i

    hc_arr = []
    hm_arr = []
    qubit_indices = list(range(nqubits))

# Exponential hamiltonians into Unitary gates that can be applied on Circuit
    if ham_mixer is not None:
        for g in gammas:
            u_ham_cost = ham_cost.exp(g)
            hc_arr.append(gates.Unitary(u_ham_cost, *qubit_indices))
        for b in betas:
            u_ham_mixer = ham_mixer.exp(b)
            hm_arr.append(gates.Unitary(u_ham_mixer, *qubit_indices))

# Construct Alternating Layers
    for circ_depth in range(0, p):
        for uhc in hc_arr:
            circuit.add(uhc)
        for uhm in hm_arr:
            circuit.add(uhm)

    return eval.qaoa_execute(circuit, datatype="complex64")
    
    '''qaoa_classical = models.QAOA(ham_cost, ham_mixer)
    initial_parameters = 0.01 * np.random.uniform(0,1,4)
    best_energy, final_parameters, extra = qaoa_classical.minimize(initial_parameters, method="BFGS")

    
    return final_parameters
    
    circ 

     add to the circuit alternative evolution of hc and hm
    for circ_depth in range(0, circ_depth):
        circuit.add(u_hc)
        if ham_mixer is not None:
            circuit.add(u_hm)
    
    return circuit

     qaoa = models.QAOA(problem_hamiltonian)
    for i in  range(0, circ_depth):
        best_energy, final_parameters, extra = qaoa.minimize(cost_function, initial_parameters, method="BFGS")
        qibo_circ = qaoa.hamiltonian.circuit(dt=dt)
    
        initial_parameters = eval.qaoa_execute(qibo_circ, runcard)

    return final_parameters'''