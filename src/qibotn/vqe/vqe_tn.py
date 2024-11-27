import numpy as np
from utils import vqe_loss_qibotn
from qibo import optimizers

class new_VQE:
    from qibo import optimizers

    def __init__(self, circuit, hamiltonian):
        """Initialize circuit ansatz and hamiltonian."""
        self.circuit = circuit
        self.hamiltonian = hamiltonian
        self.backend = hamiltonian.backend

    def new_minimize(
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
                loss_func = vqe_loss_qibotn
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
                #loss = lambda p, c, h: self.hamiltonian.backend.to_numpy(loss_func(p, c, h))
                loss = lambda p, c, h: loss_func
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
                backend=self.hamiltonian.backend
            )
            self.circuit.set_parameters(parameters)
            return result, parameters, extra

def run_vqe(circuit, hamiltonian, initial_parameters):
    from qibo import models
    #vqe = new_VQE(circuit, hamiltonian)
    #vqe.new_minimize(initial_parameters, loss_func=vqe_loss_qibotn(initial_parameters, circuit, hamiltonian))
    vqe = models.VQE(circuit, hamiltonian)
    vqe.minimize(initial_parameters, loss_func=vqe_loss_qibotn(initial_parameters, circuit, hamiltonian))
    return vqe.circuit