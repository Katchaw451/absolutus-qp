import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import DensityMatrix

def coherence_loss_circuit(metal_concentration: float, time: float) -> float:
    theta = metal_concentration * time * 0.1
    qc = QuantumCircuit(1)
    qc.ry(theta, 0)
    qc.rz(theta, 0)
    qc.ry(theta, 0)
    qc.save_statevector()  # ← obrigatório

    backend = AerSimulator()
    result = backend.run(qc).result()
    state = result.get_statevector()

    rho = DensityMatrix(state)
    coherence = np.abs(rho.data[0, 1])
    return 1 - coherence
