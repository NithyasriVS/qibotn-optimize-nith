import quimb.tensor as qtn
import quimb.tensor.tensor_core as qtnc

class MPSContractionHelper_Quimb:

    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.bra_modes = [(2 * i, 2 * i + 1, 2 * i + 2) for i in range(num_qubits)]
        offset = 2 * num_qubits + 1
        self.ket_modes = [
            (i + offset, 2 * i + 1, i + 1 + offset) for i in range(num_qubits)
        ]
    
    def _contract(self, interleaved_inputs):
        path = qtnc.contract(*interleaved_inputs, optimize=qtn.cotengra.HyperOptimizer)

        return qtnc.contract(*interleaved_inputs, optimize={"path": path})
    
    def contract_norm(self, mps_tensors, options=None):
        """Contract the corresponding tensor network to form the norm of the
        MPS.

        Parameters:
            mps_tensors: A list of rank-3 ndarray-like tensor objects.
                The indices of the ith tensor are expected to be bonding index to the i-1 tensor,
                the physical mode, and then the bonding index to the i+1th tensor.
            options: Specify the contract and decompose options.

        Returns:
            The norm of the MPS.
        """
        interleaved_inputs = []
        for i, o in enumerate(mps_tensors):
            interleaved_inputs.extend(
                [o, self.bra_modes[i], o.conj(), self.ket_modes[i]]
            )
        interleaved_inputs.append([])  # output
        return self._contract(interleaved_inputs).real
    

