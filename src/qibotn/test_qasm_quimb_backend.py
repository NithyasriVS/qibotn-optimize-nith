import random
from turtle import delay
import quimb as qu
import quimb.tensor as qtn
import numpy as np
import re

from timeit import default_timer as timer
import cirq

nqubits = 18

# define dictionary
gate_dict_cirq = {
    #'i': I,
    'h': cirq.H,
    't': cirq.T,
    #'z': Z,
    'cz': cirq.CZ,
    #'cX': cX,
    #'rz': ZPhase,
    #'rX': XPhase,
    #'x': X,
    #'y': Y,
    'x_1_2': cirq.rx(0.5*np.pi),
    'y_1_2': cirq.ry(0.5*np.pi)
    #'hz_1_2': W_1_2,
    #'fs': fSim
}

# search 'GATE_FUNCTIONS' in Source code for quimb.tensor.circuit for pre-defined gates in quimb
gate_dict = {
    #'i': I,
    'h': 'H',
    't': 'T',
    #'z': Z,
    'cz': 'cZ',
    #'cX': cX,
    #'rz': ZPhase,
    #'rX': XPhase,
    #'x': X,
    #'y': Y,
    'x_1_2': 'X_1_2',
    'y_1_2': 'Y_1_2'
}       

        
def QI_QFT(nqubits: int, with_swaps: bool = True, psi0 = None):
    ## constructs qft circuit
    #from qibo import gates
    #circuit = Circuit(nqubits)
    circ = qtn.Circuit(nqubits, psi0 = psi0)
    
    for i1 in range(nqubits):
        #circuit.add(gates.H(i1))
        circ.apply_gate('H', i1)
        for i2 in range(i1 + 1, nqubits):
            theta = np.pi / 2 ** (i2 - i1)
            #circuit.add(gates.CU1(i2, i1, theta))
            circ.apply_gate('CU1', theta, i2, i1)

    if with_swaps:
        for i in range(nqubits // 2):
            #circuit.add(gates.SWAP(i, nqubits - i - 1))
            circ.apply_gate('SWAP', i, nqubits - i - 1)

    return circ

def get_gate_params(operation):
    if "h" in operation:
        qbit_no = [int(re.findall(r'\d+', operation)[0])]
        qbit_no.insert(0, "H")
    elif "x" in operation:
        qbit_no = [int(re.findall(r'\d+', operation)[0])]
        qbit_no.insert(0, "X")
    elif "y" in operation:
        qbit_no = [int(re.findall(r'\d+', operation)[0])]
        qbit_no.insert(0, "Y")
    elif "z" in operation:
        qbit_no = [int(re.findall(r'\d+', operation)[0])]
        qbit_no.insert(0, "Z")
    elif "s" in operation:
        qbit_no = [int(re.findall(r'\d+', operation)[0])]
        qbit_no.insert(0, "S")
    elif "t" in operation:
        qbit_no = [int(re.findall(r'\d+', operation)[0])]
        qbit_no.insert(0, "T")
    elif "cu1" in operation:
        lamda = float('.'.join(re.findall(r'\b\d+(?:[Ee][+-]?\d+)?', 
                                          operation.split(" ")[0])))
        qbit_no = re.findall(r'\d+', operation.split(" ")[1])
        qbit_no = [int(x) for x in qbit_no]
        qbit_no[0:0] = ["CU1", lamda]
    elif "cu2" in operation:
        angles = re.findall(r'\b\d+(?:[Ee][+-]?\d+)?',operation.split(" ")[0])
        phi = float('.'.join(angles[0:2]))
        lamba = float('.'.join(angles[2:]))
        qbit_no = re.findall(r'\d+', operation.split(" ")[1])
        qbit_no = [int(x) for x in qbit_no]
        qbit_no[0:0] = ["CU2", phi, lamda]
    elif "cu3" in operation:
        angles = re.findall(r'\b\d+(?:[Ee][+-]?\d+)?',operation.split(" ")[0])
        theta = float('.'.join(angles[0:2]))
        phi = float('.'.join(angles[2:4]))
        lamba = float('.'.join(angles[4:]))
        qbit_no = re.findall(r'\d+', operation.split(" ")[1])
        qbit_no = [int(x) for x in qbit_no]
        qbit_no[0:0] = ["CU3", theta, phi, lamda]       
    elif "cx" in operation:
        qbit_no = re.findall(r'\d+', operation.split(" ")[1])
        qbit_no = [int(x) for x in qbit_no]
        qbit_no.insert(0, "CX")
    elif "cy" in operation:
        qbit_no = re.findall(r'\d+', operation.split(" ")[1])
        qbit_no = [int(x) for x in qbit_no]
        qbit_no.insert(0, "CY") 
    elif "cz" in operation:
        qbit_no = re.findall(r'\d+', operation.split(" ")[1])
        qbit_no = [int(x) for x in qbit_no]
        qbit_no.insert(0, "CZ")
    elif "rx" in operation:
        theta = float('.'.join(re.findall(r'\b\d+(?:[Ee][+-]?\d+)?', 
                                          operation.split(" ")[0])))
        qbit_no = [int(re.findall(r'\d+', operation)[0])]
        qbit_no[0:0] = ["RX", theta]
    elif "ry" in operation:
        theta = float('.'.join(re.findall(r'\b\d+(?:[Ee][+-]?\d+)?', 
                                          operation.split(" ")[0])))
        qbit_no = [int(re.findall(r'\d+', operation)[0])]
        qbit_no[0:0] = ["RY", theta]
    elif "rz" in operation:
        theta = float('.'.join(re.findall(r'\b\d+(?:[Ee][+-]?\d+)?', 
                                          operation.split(" ")[0])))
        qbit_no = [int(re.findall(r'\d+', operation)[0])]
        qbit_no[0:0] = ["RZ", theta]
    elif "rzz" in operation:
        theta = float('.'.join(re.findall(r'\b\d+(?:[Ee][+-]?\d+)?', 
                                          operation.split(" ")[0])))
        qbit_no = re.findall(r'\d+', operation.split(" ")[1])
        qbit_no = [int(x) for x in qbit_no]
        qbit_no[0:0] = ["RZZ", theta]
    elif "u1" in operation:
        lamda = float('.'.join(re.findall(r'\b\d+(?:[Ee][+-]?\d+)?', 
                                          operation.split(" ")[0])))
        qbit_no = [int(re.findall(r'\d+', operation)[0])]
        qbit_no[0:0] = ["U1", lamda]
    elif "u2" in operation:
        angles = re.findall(r'\b\d+(?:[Ee][+-]?\d+)?',operation.split(" ")[0])
        phi = float('.'.join(angles[0:2]))
        lamba = float('.'.join(angles[2:]))
        qbit_no = int(re.findall(r'\d+', operation)[0])
        qbit_no[0:0] = ["U2", phi, lamda]
    elif "u3" in operation:
        angles = re.findall(r'\b\d+(?:[Ee][+-]?\d+)?',operation.split(" ")[0])
        theta = float('.'.join(angles[0:2]))
        phi = float('.'.join(angles[2:4]))
        lamba = float('.'.join(angles[4:]))
        qbit_no = int(re.findall(r'\d+', operation)[0])
        qbit_no[0:0] = ["U3", theta, phi, lamda]
    else:
        assert("Unsupported gate")

    return qbit_no


def get_gate_functions(qasm_str, start_idx):
    # func_list = []
    # param_list = {}
    # for line in qasm_str[start_idx:]:
    #     if "gate" in line:
    #         line = line.split(" ")
    #         for i in line[3:]:
    #             if ',' in i:
    #                 params = i.split(",")
    #                 param_list.append([int(j) for j in params])
    #             elif "(" in i:
    #                 params = re.findall(r'\w+', i)
    #                 param_list.append([int(j) for j in params])
    #             elif "{" in i:
    #                 break
    #     elif "}" in line:
    #         return func_list
    #     else:
    #         func_list.append(line)
    pass

def qasm_QFT(nqubits:int, qasm_str:str, with_swaps: bool = True, psi0 = None):
    circ = qtn.Circuit(nqubits, psi0 = psi0)
    # circ = qtn.Circuit.qasm(nqubits, psi0 = psi0)
    gate_functions = {}
    qasm_str = qasm_str.split('\n')
    for idx, line in enumerate(qasm_str):
        command = line.split(" ")[0]
        if re.search("include|//|OPENQASM", command):
            continue
        elif "qreg" in command:
            nbits = int(re.findall(r'\d+', line)[0])
            assert(nbits == nqubits)
        elif "swap" in command:
            break
        elif "gate" in command:      # TODO: Complete gate handling
            gate_name = line.split(" ")[1]
            # gate_func = get_gate_functions(qasm_str, idx)
            # gate_funtions[gate_name] = gate_func
            pass
        elif "barrier" in command:   # TODO: Complete barrier handling
            pass
        elif "measure" in command:   # TODO: Complete measure handling
            pass
        else:
            params = get_gate_params(line)
            circ.apply_gate(*params)

    if with_swaps:
        for i in range(nqubits // 2): # TODO: Ignore the barrier indices? 
            circ.apply_gate('SWAP', i, nqubits - i - 1)

    return circ


def eval_QI_qft(nqubits, bond_dim=0, backend='numpy', qibo_backend='numpy', 
                with_swaps=True, compare_qibo=False):
    # backend (quimb): numpy, cupy, jax. Passed to ``opt_einsum``.
    # qibo_backend: qibojit, qibotf, tensorflow, numpy
    
    # generate random statevector as initial state
    init_state = np.random.random(2 ** nqubits) + 1j 
                    * np.random.random(2 ** nqubits)
    init_state = init_state / np.sqrt((np.abs(init_state)**2).sum())
    
    # Qibo part
    if compare_qibo==True:
        import qibo
        qibo.set_backend(qibo_backend)
        # qibo.set_backend(backend="qibojit", platform="numba")
        from qibo.models import QFT as qibo_qft
        start = timer()
        circ_qibo = qibo_qft(nqubits, with_swaps)
        amplitudes_reference = np.array(circ_qibo(init_state))
        end = timer()
        print("qibo time is " + str(end-start))
        qasm_circ = circ_qibo.to_qasm()

 
    #####################################################################
    
    # Quimb part
    qtn.tensor_core.set_contract_backend(backend)
    ## convert vector to MPS
    dims = tuple(2*np.ones(nqubits, dtype=int))
    start = timer() 
    init_state_MPS = 
        qtn.tensor_1d.MatrixProductState.from_dense(init_state, dims)
    end = timer()
    MPS_time = end-start
    # print('MPS conversion time: ', MPS_time)
    
    # construct quimb qft circuit
    start = timer()
    if compare_qibo == True:
        circ_quimb = 
            qasm_QFT(nqubits, qasm_circ, with_swaps, psi0=init_state_MPS)
    else:
        circ_quimb = QI_QFT(nqubits, with_swaps, psi0=init_state_MPS)

    result = circ_quimb.to_dense(backend=backend)
    amplitudes = result.flatten()
    end = timer()
    quimb_qft_time = end-start
    print("quimb time is " + str(quimb_qft_time))
    assert(np.allclose(amplitudes,amplitudes_reference))

if __name__ == '__main__':
    print("Testing for %d nqubits" % (nqubits))
    result = eval_QI_qft(nqubits, compare_qibo=True)