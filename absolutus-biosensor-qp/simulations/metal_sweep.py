import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.coherence_detector import coherence_loss_circuit
import matplotlib.pyplot as plt
import numpy as np

concentrations = np.linspace(0, 100, 100)  # µM
time = 1.5  # min

losses = [coherence_loss_circuit(c, time) for c in concentrations]

plt.plot(concentrations, losses)
plt.xlabel("Concentração de Cd²⁺ (µM)")
plt.ylabel("Perda de Coerência")
plt.title("Resposta do Biosensor Quântico")
plt.grid(True)
plt.savefig("sensor_response.png")
