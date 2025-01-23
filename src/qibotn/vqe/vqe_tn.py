import numpy as np
from utils import vqe_loss_qibotn, vqe_loss_qibotn_2
from qibo import models

def run_vqe(circuit, hamiltonian, initial_parameters):
    
    vqe = models.VQE(circuit, hamiltonian)
    vqe.minimize(initial_parameters, loss_func=vqe_loss_qibotn(initial_parameters, circuit, hamiltonian))
    return vqe.circuit