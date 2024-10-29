import qibo
from qibo import models, hamiltonians, Circuit, gates
from qibo.models.utils import vqe_loss
import numpy as np

class VQE_for_qibotn:
    
    def __init__(self, circuit, hamiltonian):
        """Initialize circuit ansatz and hamiltonian."""
        self.circuit = circuit
        self.hamiltonian = hamiltonian
        self.backend = hamiltonian.backend

    def minimize_qibotn(
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
            loss_func = vqe_loss
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
    
import numpy as np
from qibo.symbols import X, Y, Z
import qibo

computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": False,
    "NCCL_enabled": False,
    "expectation_enabled": False
}
qibo.set_backend(backend="qibotn", platform="qutensornet", runcard=computation_settings)

vqe_ansatz = models.Circuit(2)
vqe_ansatz.add(gates.RY(0, theta=0))
hamiltonian = hamiltonians.XXZ(2)
initial_parameters = np.random.uniform(0, 2, 1)

v_m = models.VQE_for_qibotn(vqe_ansatz, hamiltonian)
v_m.minimize_qibotn(initial_parameters)
c = v_m.circuit

result = c()

print(result.state())
