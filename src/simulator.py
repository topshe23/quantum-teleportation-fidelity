# src/simulator.py
# Runs quantum circuits using Qiskit Aer simulators

from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit import transpile


def run_statevector(circuit):
    """
    Ideal simulation — no noise, no shots.
    Returns the exact probability of measuring |1> on bob_bit.
    """
    sim = AerSimulator(method='statevector')
    compiled = transpile(circuit, sim)
    result = sim.run(compiled).result()
    counts = result.get_counts()
    return counts


def run_qasm(circuit, shots=1024):
    """
    Shot-based simulation — like a real device.
    Returns counts dict e.g. {'0': 810, '1': 214}
    """
    sim = AerSimulator(method='statevector')
    compiled = transpile(circuit, sim)
    result = sim.run(compiled, shots=shots).result()
    counts = result.get_counts()
    return counts


def run_with_noise(circuit, noise_level, shots=1024):
    """
    Adds depolarizing noise to every gate.
    noise_level: float between 0.0 (no noise) and 0.1 (heavy noise)
    Returns counts dict.
    """
    # Build noise model
    noise_model = NoiseModel()
    error_1q = depolarizing_error(noise_level, 1)        # single-qubit gate error
    error_2q = depolarizing_error(noise_level * 2, 2)    # two-qubit gate error (always higher)

    noise_model.add_all_qubit_quantum_error(error_1q, ['h', 'ry', 'rz', 'x', 'z'])
    noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])

    sim = AerSimulator(noise_model=noise_model)
    compiled = transpile(circuit, sim)
    result = sim.run(compiled, shots=shots).result()
    counts = result.get_counts()
    return counts