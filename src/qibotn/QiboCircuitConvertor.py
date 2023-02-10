
import cupy as cp
import numpy as np

EINSUM_SYMBOLS_BASE = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

class QiboCircuitToEinsum:
    def __init__(self, circuit, dtype='complex128'):
        
        self.backend = cp
        self.dtype   = getattr(self.backend, dtype)

        self.input_tensor_counter = np. zeros((circuit.nqubits,))
        self.gates = []
        for gate in circuit.queue:
            targets = list(gate.target_qubits)
            for target in targets:
                self.input_tensor_counter[target] = self.input_tensor_counter[target] + 1
            controls = list(gate.control_qubits)
            for control in controls:
                self.input_tensor_counter[control] = self.input_tensor_counter[control] + 1
            gate_qubits = controls + targets
            self.gates.append((cp.asarray(gate.matrix).reshape((2,) * 2 * len(gate_qubits)), gate_qubits))

        self.qubit_name = [indx for indx, value in enumerate(self.input_tensor_counter) if value > 0]

    def state_vector(self):

        input_tensor_count = np.count_nonzero(self.input_tensor_counter)

        input_operands = self._get_bitstring_tensors('0'*input_tensor_count, self.dtype, backend=self.backend)
        
        mode_labels, qubits_frontier, next_frontier = self._init_mode_labels_from_qubits(self.qubit_name)

        gate_mode_labels, gate_operands = self._parse_gates_to_mode_labels_operands(self.gates, 
                                                                      qubits_frontier, 
                                                                       next_frontier)

        operands = input_operands + gate_operands
        mode_labels += gate_mode_labels

        expression = self._convert_mode_labels_to_expression(mode_labels, qubits_frontier)

        return expression, operands

    def _get_symbol(self,i):
        """
        Return a Unicode as label for index.

        .. note:: This function is adopted from `opt_einsum <https://optimized-einsum.readthedocs.io/en/stable/_modules/opt_einsum/parser.html#get_symbol>`_
        """
        if i < 52:
            return EINSUM_SYMBOLS_BASE[i]
        return chr(i + 140)

    def _init_mode_labels_from_qubits(self,qubits):

        frontier_dict ={}
        n = len(qubits)
        for x in range(n):
            frontier_dict[qubits[x]]=x
        return [[i] for i in range(n)], frontier_dict, n

    def _get_bitstring_tensors(self, bitstring, dtype=np.complex128, backend=cp):

        asarray = backend.asarray #_get_backend_asarray_func(backend)
        state_0 = asarray([1, 0], dtype=dtype)
        state_1 = asarray([0, 1], dtype=dtype)

        basis_map = {'0': state_0,
                    '1': state_1}
        
        operands = [basis_map[ibit] for ibit in bitstring]
        return operands

    def _parse_gates_to_mode_labels_operands(
        self,
        gates, 
        qubits_frontier, 
        next_frontier
    ):

        mode_labels = []
        operands = []

        for tensor, gate_qubits in gates:
            operands.append(tensor)
            input_mode_labels = []
            output_mode_labels = []
            for q in gate_qubits:
                input_mode_labels.append(qubits_frontier[q])
                output_mode_labels.append(next_frontier)
                qubits_frontier[q] = next_frontier
                next_frontier += 1
            mode_labels.append(output_mode_labels+input_mode_labels)
        return mode_labels, operands

    def _convert_mode_labels_to_expression(self,input_mode_labels, output_mode_labels):
   
        out_list = []
        for key in output_mode_labels:
            out_list.append(output_mode_labels[key])

        input_symbols = [''.join(map(self._get_symbol, idx)) for idx in input_mode_labels]
        expression = ','.join(input_symbols) + '->' + ''.join(map(self._get_symbol, out_list)) 

        return expression
