# Loss function for Variational Quantum Eigensolver
loss_tracker = []

def vqe_loss_qibotn(p, c, h):
        def loss_return(p, c, h):
                c.set_parameters(p)
                result = h.backend.execute_circuit(c)
                final_state = result.state()
                final_state = final_state.get()
                loss_tracker.append(h.expectation(final_state))
                return h.expectation(final_state)
        return loss_return

def plot_result():
        import matplotlib.pyplot as plt

        plt.plot(range(len(loss_tracker)), loss_tracker)
        plt.xlabel('Iteration')
        plt.ylabel('Loss')
        plt.title('Expectation Value Fluctuations During Minimization')
        plt.show()