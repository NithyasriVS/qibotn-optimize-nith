from qibo.backends.numpy import NumpyBackend
from qibo.config import raise_error
from qibo.result import QuantumState
import tebd as tbd


class QuimbBackend(NumpyBackend):

    def __init__(self, runcard):
        super().__init__()
        import quimb  # pylint: disable=import-error

        if runcard is not None:
            self.MPI_enabled = runcard.get("MPI_enabled", False)
            self.NCCL_enabled = runcard.get("NCCL_enabled", False)
            self.expectation_enabled = runcard.get("expectation_enabled", False)

            mps_enabled_value = runcard.get("MPS_enabled")
            if mps_enabled_value is True:
                self.mps_opts = {"method": "svd", "cutoff": 1e-6, "cutoff_mode": "abs"}
            elif mps_enabled_value is False:
                self.mps_opts = None
            elif isinstance(mps_enabled_value, dict):
                self.mps_opts = mps_enabled_value
            else:
                raise TypeError("MPS_enabled has an unexpected type")
            
            tebd_enabled_value = runcard.get("TEBD_enabled")
            if tebd_enabled_value is True:
                self.tebd_opts = {"dt":1e-2, "hamiltonian": "XXZ"}
            elif tebd_enabled_value is False:
                self.tebd_opts = None
            elif isinstance(tebd_enabled_value, dict):
                self.tebd_opts = mps_enabled_value

        else:
            self.MPI_enabled = False
            self.MPS_enabled = False
            self.NCCL_enabled = False
            self.expectation_enabled = False
            self.mps_opts = None
            self.tebd_opts = None

        self.name = "qibotn"
        self.quimb = quimb
        self.platform = "QuimbBackend"
        self.versions["quimb"] = self.quimb.__version__

    def apply_gate(self, gate, state, nqubits):  # pragma: no cover
        raise_error(NotImplementedError, "QiboTN cannot apply gates directly.")

    def apply_gate_density_matrix(self, gate, state, nqubits):  # pragma: no cover
        raise_error(NotImplementedError, "QiboTN cannot apply gates directly.")

    def assign_measurements(self, measurement_map, circuit_result):
        raise_error(NotImplementedError, "Not implemented in QiboTN.")

    def set_precision(self, precision):
        if precision != self.precision:
            super().set_precision(precision)

    def execute_circuit(
        self, circuit, initial_state=None, nshots=None, return_array=False
    ):  # pragma: no cover
        """Executes a quantum circuit.

        Args:
            circuit (:class:`qibo.models.circuit.Circuit`): Circuit to execute.
            initial_state (:class:`qibo.models.circuit.Circuit`): Circuit to prepare the initial state.
                If ``None`` the default ``|00...0>`` state is used.

        Returns:
            QuantumState or numpy.ndarray: If `return_array` is False, returns a QuantumState object representing the quantum state. If `return_array` is True, returns a numpy array representing the quantum state.
        """

        import qibotn.eval_qu as eval

        if self.MPI_enabled == True:
            raise_error(NotImplementedError, "QiboTN quimb backend cannot support MPI.")
        if self.NCCL_enabled == True:
            raise_error(
                NotImplementedError, "QiboTN quimb backend cannot support NCCL."
            )
        if self.expectation_enabled == True:
            raise_error(
                NotImplementedError, "QiboTN quimb backend cannot support expectation"
            )
        if self.tebd_enabled == True:

            from qibo import hamiltonians
            from qibo.hamiltonians import SymbolicHamiltonian

            ham = self.tebd_opts["hamiltonian"]
            dt = self.tebd_opts["dt"]
            nqubits = circuit.nqubits

            if ham == "TFIM":
                ham = hamiltonians.TFIM(nqubits=nqubits, dense=False)
            elif ham == "NIX":
                ham = hamiltonians.X(nqubits=nqubits, dense=False)
            elif ham == "NIY":
                ham = hamiltonians.Y(nqubits=nqubits, dense=False)
            elif ham == "NIZ":
                ham = hamiltonians.Z(nqubits=nqubits, dense=False)
            elif ham == "XXZ":
                ham = hamiltonians.XXZ(nqubits=nqubits, dense=False)
            elif ham == "MC":
                ham = hamiltonians.MaxCut(nqubits=nqubits, dense=False)
            
            # Extraction of terms

            terms_list = []
            list_of_terms = ham.terms
            for t in list_of_terms:
                terms_list.append(t.matrix)
            
            fullmatrix = ham.matrix
             
            # Actual TEBD invocation codes below
            print("Add code for TEBD function invocation here")
            #[NOT RELEVANT FOR ABOVE APPROACH] local_unitary = tbd.handle_unitary(circuit) # pseudocode
            
            '''#state = call some fn which must be written in eval_qu to do 
            # tbd.do_tebd(terms_list, dt) something like this within eval_qu because I'll need these 2 params in tebd.py or just send
            # the terms_list and self.tebd_opts - anything else required must see as we progress
            
            # in eval_qu: a fn that will do tebd and store values of dense vector at diff times
            # in a log file and finally only return the evolved dense vector using .to_dense'''
        
        state = eval.dense_vector_tn_qu(
            circuit.to_qasm(), initial_state, self.mps_opts, backend="numpy"
        )

        if return_array:
            return state.flatten()
        else:
            return QuantumState(state.flatten())
