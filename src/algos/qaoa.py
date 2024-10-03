import qibo
from qibo import hamiltonians, gates, Circuit

def prepare_qaoa_circuit(circuit, runcard, nqubits):

    ham_cost = runcard["Hcost"]
    ham_mixer = runcard["Hmixer"] # can be None
    circ_depth = runcard["circ_depth"]
    gamma = runcard["cost_evolution_param"]
    beta = runcard["mixer_evolution_param"] # can be None
    
    qubits = list(range(nqubits))
    evol_hc = ham_cost.exp(gamma)
    u_hc = gates.Unitary(evol_hc, *qubits)

    if ham_mixer is not None:
        evol_hm = ham_mixer.exp(gamma)
        u_hm = gates.Unitary(evol_hm, *qubits)

    # add to the circuit alternative evolution of hc and hm
    for circ_depth in range(0, circ_depth):
        circuit.add(u_hc)
        if ham_mixer is not None:
            circuit.add(u_hm)
    
    return circuit



    

