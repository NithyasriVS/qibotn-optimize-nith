import qibo
from qibo import hamiltonians

# user defines the number of qubits they want
nqubits = 4
# user defines their hamiltonian using qibo
hamiltonian = hamiltonians.XXZ(nqubits)

'''Computation settings for TEBD

    H: a qibo hamiltonian object
    nqubits: number of qubits
    dt: time step for evolution
    opts: physical quantity to evaluate (available options are: entropy, zmag, schmidtgap)

'''

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
            "H": hamiltonian,
            "nqubits": nqubits,
            "dt": 1e-3,
            "opts": "entropy"
        },
        "NCCL_enabled": False,
        "expectation_enabled": False
    }

qibo.set_backend(backend="qibotn", platform="qutensornet", runcard=computation_settings)

hamiltonian = hamiltonians.XXZ(nqubits)



