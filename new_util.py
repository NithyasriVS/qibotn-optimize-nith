import numpy as np

def vqe_loss_qibotn(p, c, h):

        c.set_parameters(p)
        result = h.backend.execute_circuit(c)
        final_state = result.state()
        final_state = final_state.get()
        dtype = np.float64
        return h.expectation(final_state)