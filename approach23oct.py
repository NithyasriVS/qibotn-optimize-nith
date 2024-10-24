import numpy as np
from qibo import hamiltonians, Circuit, models
from qibo.symbols import X, Y, Z
#import qibotn.eval as eval

dt = 0.1
p = 5 #depth
#hamiltonian = sum([X(0) * X(1), Y(0) * Y(1), 0.5 * Z(0) * Z(1)])
#hamiltonian = hamiltonians.SymbolicHamiltonian(hamiltonian)
hamiltonian = hamiltonians.SymbolicHamiltonian(X(0)*X(1))
#mixer = sum([0.5 * Z(0) * Z(1), X(0) * X(1), Y(0) * Y(1)])
#mix = hamiltonians.SymbolicHamiltonian(mixer)

qaoa = models.QAOA(hamiltonian)
initial_parameters = 0.01 * np.random.random(4)
best_energy, final_parameters, extra = qaoa.minimize(initial_parameters, method="BFGS")


#dense_vector_hamiltonian = #output from running qaoa.hamiltonian.circuit(dt=dt) on qibotn eval.py
for i in  range(0, p):
    best_energy, final_parameters, extra = qaoa.minimize(initial_parameters, method="BFGS")
    circuit = qaoa.hamiltonian.circuit(dt=dt)
    #initial_parameters = eval.qaoa_execute(qibo_circ, runcard_qaoa, nqubits)


