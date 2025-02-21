# Loss function for Variational Quantum Eigensolver
loss_tracker = []
import cupy as cp

def vqe_loss_qibotn(p, c, h):
        def loss_return(p, c, h):
                global loss_tracker
                c.set_parameters(p)
                result = h.backend.execute_circuit(c)
                final_state = result.state()
                final_state = final_state.get()
                loss_value = h.expectation(final_state)
                if isinstance(loss_value, cp.ndarray):
                        loss_value = loss_value.get()
                loss_tracker.append(loss_value)
                return loss_value
        return loss_return

def plot_result():
        import matplotlib.pyplot as plt

        global loss_tracker
        plt.plot(range(len(loss_tracker)), loss_tracker)
        plt.xlabel('Iteration')
        plt.ylabel('Loss')
        plt.title('Expectation Value Fluctuations During Minimization')
        plt.savefig("graphyay")