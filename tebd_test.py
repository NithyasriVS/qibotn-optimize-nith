def main():

    import numpy as np
    from qibo import Circuit, gates, models
    import qibo

    import quimb
    import quimb.tensor as qtn

    #import qibotn_dependency as qd
    from qibotn import eval_qu as evqu

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
            "H": qtn.ham_1d_heis(44),
            "dt": 1e-3
        },
        "NCCL_enabled": False,
        "expectation_enabled": False,
    }

    qibo.set_backend(backend="qibotn", platform="qutensornet", runcard=computation_settings)

    circuit = models.Circuit(44)

    circuit.add(gates.X(14))
    circuit.add(gates.X(29))

    result = circuit()

    print(result.state())


if __name__ == "__main__":
    main()

