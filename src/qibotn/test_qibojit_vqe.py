import qibo
from qibo import models, Circuit, hamiltonians, gates
import numpy as np

def vqe_loss_qtest(params, circuit, hamiltonian):
    circuit.set_parameters(params)
    #hamiltonian.backend = "CuTensorNet"
    result = hamiltonian.backend.execute_circuit(circuit)
    print("result and its type: ", result," ",type(result))
    final_state = result.state()
    print("final state and its type: ", final_state, " ", type(final_state))
    print("expectation: ",hamiltonian.expectation(final_state))
    print("FInal return: ",hamiltonian.expectation(final_state), " type: ", type(hamiltonian.expectation(final_state)))
    return hamiltonian.expectation(final_state)

class VQE_qtest:
    """This class implements the variational quantum eigensolver algorithm.

    Args:
        circuit (:class:`qibo.models.circuit.Circuit`): Circuit that
            implements the variaional ansatz.
        hamiltonian (:class:`qibo.hamiltonians.Hamiltonian`): Hamiltonian object.

    Example:
        .. testcode::

            import numpy as np
            from qibo import gates, models, hamiltonians
            # create circuit ansatz for two qubits
            circuit = models.Circuit(2)
            circuit.add(gates.RY(0, theta=0))
            # create XXZ Hamiltonian for two qubits
            hamiltonian = hamiltonians.XXZ(2)
            # create VQE model for the circuit and Hamiltonian
            vqe = models.VQE(circuit, hamiltonian)
            # optimize using random initial variational parameters
            initial_parameters = np.random.uniform(0, 2, 1)
            vqe.minimize(initial_parameters)
    """

    from qibo import optimizers

    def __init__(self, circuit, hamiltonian):
        """Initialize circuit ansatz and hamiltonian."""
        self.circuit = circuit
        self.hamiltonian = hamiltonian
        self.backend = hamiltonian.backend

    def minimize_qtest(
        self,
        initial_state,
        method="Powell",
        loss_func=None,
        jac=None,
        hess=None,
        hessp=None,
        bounds=None,
        constraints=(),
        tol=None,
        callback=None,
        options=None,
        compile=False,
        processes=None,
    ):
        
        if loss_func is None:
            loss_func = vqe_loss_qtest
        if compile:
            loss = self.hamiltonian.backend.compile(loss_func)
        else:
            loss = loss_func

        if method == "cma":
            # TODO: check if we can use this shortcut
            # dtype = getattr(self.hamiltonian.backend.np, self.hamiltonian.backend._dtypes.get('DTYPE'))
            dtype = self.hamiltonian.backend.np.float64
            loss = (
                (lambda p, c, h: loss_func(p, c, h).item())
                if str(dtype) == "torch.float64"
                else (lambda p, c, h: dtype(loss_func(p, c, h)))
            )
        elif method != "sgd":
            loss = lambda p, c, h: self.hamiltonian.backend.to_numpy(loss_func(p, c, h))
        result, parameters, extra = self.optimizers.optimize(
            loss,
            initial_state,
            args=(self.circuit, self.hamiltonian),
            method=method,
            jac=jac,
            hess=hess,
            hessp=hessp,
            bounds=bounds,
            constraints=constraints,
            tol=tol,
            callback=callback,
            options=options,
            compile=compile,
            processes=processes,
            backend=self.hamiltonian.backend,
        )
        self.circuit.set_parameters(parameters)
        return result, parameters, extra

qibo.set_backend(backend="qibojit")

nqubits = 2
circ = Circuit(nqubits)
circ.add(gates.RX(0,0))
circ.add(gates.RX(1,0))

ham = hamiltonians.XXZ(nqubits)
initial_parameters = 0.01 * np.random.random(nqubits)

#ham.backend = "qibotf"

vqe = VQE_qtest(circ, ham)
print(vqe.minimize_qtest(initial_parameters, loss_func=vqe_loss_qtest))



