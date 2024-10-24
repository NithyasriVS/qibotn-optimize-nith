import qibo
from qibo import hamiltonians, models, gates, Circuit
import numpy as np
import qibotn.eval as eval

def prepare_qaoa_circuit(runcard):

    problem_hamiltonian = runcard["Hcost"]
    #ham_mixer = runcard["Hmixer"] # optional
    circ_depth = runcard["circ_depth"]
    initial_parameters = runcard["init_params"]
    dt = runcard["dt"]

    qaoa = models.QAOA(problem_hamiltonian)
    for i in  range(0, circ_depth):
        best_energy, final_parameters, extra = qaoa.minimize(initial_parameters, method="BFGS")
        qibo_circ = qaoa.hamiltonian.circuit(dt=dt)
    
        initial_parameters = eval.qaoa_execute(qibo_circ, runcard)

    return final_parameters

    '''qubits = list(range(nqubits))
    evol_hc = ham_cost.exp(gamma)
    # evol_hc = ham_cost.exp(-1*np.i*gamma)
    u_hc = gates.Unitary(evol_hc, *qubits)

    if ham_mixer is not None:
        evol_hm = ham_mixer.exp(gamma)
        u_hm = gates.Unitary(evol_hm, *qubits)
    
    qaoa_classical = models.QAOA(ham_cost, ham_mixer)
    initial_parameters = 0.01 * np.random.uniform(0,1,4)
    best_energy, final_parameters, extra = qaoa_classical.minimize(initial_parameters, method="BFGS")

    
    return final_parameters
    
    circ 

     add to the circuit alternative evolution of hc and hm
    for circ_depth in range(0, circ_depth):
        circuit.add(u_hc)
        if ham_mixer is not None:
            circuit.add(u_hm)
    
    return circuit'''