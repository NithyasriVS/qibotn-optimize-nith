import numpy as np

from qibo.config import raise_error
from qibo.models.evolution import StateEvolution
from qibo.models.utils import vqe_loss


class VQE:

    from qibo import optimizers

    def __init__(self, circuit, hamiltonian):
        """Initialize circuit ansatz and hamiltonian."""
        self.circuit = circuit
        self.hamiltonian = hamiltonian
        self.backend = hamiltonian.backend

    def minimize(
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

    def energy_fluctuation(self, state):
        """
        Evaluate energy fluctuation

        .. math::
            \\Xi_{k}(\\mu) = \\sqrt{\\langle\\mu|\\hat{H}^2|\\mu\\rangle - \\langle\\mu|\\hat{H}|\\mu\\rangle^2} \\,

        for a given state :math:`|\\mu\\rangle`.

        Args:
            state (np.ndarray): quantum state to be used to compute the energy fluctuation with H.
        """
        return self.hamiltonian.energy_fluctuation(state)