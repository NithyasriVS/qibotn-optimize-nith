import numpy as np
from qibo import Circuit, gates, hamiltonians
import qibo

ham = hamiltonians.TFIM(nqubits=5, dense=False)
circuit = ham.circuit(dt=1e-2)

qasm = circuit.to_qasm()

print(qasm)

'''
Conclusion: Must add support for Unitary in qibo for openqasm
Finding: NotImplementedError: Unitary is not supported by OpenQASM
'''