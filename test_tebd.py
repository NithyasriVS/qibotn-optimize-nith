import numpy as np
from qibo import Circuit, gates, models, callbacks
import qibo

computation_settings = {
    "MPI_enabled": False,
    "MPS_enabled": {
        "qr_method": False,
        "svd_method": {
            "partition": "UV",
            "abs_cutoff": 1e-12,
        },
    },
    "TEBD_enabled": {
        "H": "<LocalHam1D(L=44, cyclic=False)>",
        "dt": 1e-3
    },
    "NCCL_enabled": False,
    "expectation_enabled": False,
}


qibo.set_backend(backend="qibotn", platform="qutensornet", runcard=computation_settings)


c = Circuit(2)
# Add some gates
c.add(gates.H(0))
c.add(gates.H(1))

result = c()

print(result.state())