# Loss function for Variational Quantum Eigensolver

def vqe_loss_qibotn(p, c, h):
        def loss_return(p, c, h):
                c.set_parameters(p)
                result = h.backend.execute_circuit(c)
                final_state = result.state()
                final_state = final_state.get()
                return h.expectation(final_state)
        return loss_return