# Loss function for Variational Quantum Eigensolver
loss_tracker = []
import cupy as cp
import re

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
        plt.savefig("graphn5")

def calc_final_measurement(measurement_str):
        p_max = 0
        bitstr_max = ""
        measurement_format = r'\(?([\d\.\-e\+j]+)\)?\|([01]+)>'
        
        matching = re.findall(measurement_format, measurement_str)
        for prob, measurement in matching:
                prob = complex(prob) #extract probability as complex number
        
                prob = abs(prob) ** 2  
                if prob > p_max:
                        p_max = prob
                final_output = measurement
        return final_output