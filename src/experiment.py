# src/experiment.py
# Sweeps parameters and records fidelity data

import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.circuit import create_teleportation_circuit
from src.simulator import run_qasm, run_with_noise
from src.utils import compute_fidelity, save_results, plot_graph


def experiment_noise_vs_fidelity(shots=8192):
    """
    Experiment 1: How does noise level affect fidelity?
    Uses theta=pi/3 (theoretical prob=0.25) for clearer signal.
    Sweeps depolarizing noise from 0.0 to 0.3
    """
    print("Running Experiment 1: Noise vs Fidelity...")

    noise_levels = [0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20, 0.25, 0.30]
    fidelities = []
    theta = np.pi / 3  # theoretical prob = sin(pi/6)^2 = 0.25

    for noise in noise_levels:
        qc, _ = create_teleportation_circuit(state_angle_theta=theta)
        if noise == 0.0:
            counts = run_qasm(qc, shots=shots)
        else:
            counts = run_with_noise(qc, noise_level=noise, shots=shots)
        fidelity = compute_fidelity(counts, theta=theta)
        fidelities.append(fidelity)
        print(f"  noise={noise:.2f} -> fidelity={fidelity:.4f}")

    return noise_levels, fidelities
def experiment_shots_vs_fidelity():
    """
    Experiment 2: How does number of shots affect fidelity stability?
    More shots = more stable result.
    """
    print("Running Experiment 2: Shots vs Fidelity...")

    shot_counts = [64, 128, 256, 512, 1024, 2048, 4096]
    fidelities = []
    theta = np.pi / 2

    for shots in shot_counts:
        qc, _ = create_teleportation_circuit(state_angle_theta=theta)
        counts = run_qasm(qc, shots=shots)
        fidelity = compute_fidelity(counts, theta=theta)
        fidelities.append(fidelity)
        print(f"  shots={shots} -> fidelity={fidelity:.4f}")

    return shot_counts, fidelities


def experiment_theta_vs_fidelity(shots=1024):
    """
    Experiment 3: Does fidelity hold across different input states?
    Sweeps theta from 0 to pi.
    """
    print("Running Experiment 3: Theta vs Fidelity...")

    thetas = np.linspace(0.1, np.pi, 12)
    fidelities = []

    for theta in thetas:
        qc, _ = create_teleportation_circuit(state_angle_theta=theta)
        counts = run_qasm(qc, shots=shots)
        fidelity = compute_fidelity(counts, theta=theta)
        fidelities.append(fidelity)
        print(f"  theta={theta:.3f} -> fidelity={fidelity:.4f}")

    return list(thetas), fidelities


if __name__ == "__main__":

    # --- Run all 3 experiments ---
    noise_levels, fidelities_noise = experiment_noise_vs_fidelity()
    shot_counts, fidelities_shots = experiment_shots_vs_fidelity()
    thetas, fidelities_theta = experiment_theta_vs_fidelity()

    # --- Save CSV ---
    save_results(
        {'noise_level': noise_levels, 'fidelity': fidelities_noise},
        'results/data/results.csv'
    )

    # --- Plot 1: Noise vs Fidelity ---
    plot_graph(
        x=noise_levels,
        y=fidelities_noise,
        xlabel='Depolarizing Noise Level',
        ylabel='Fidelity',
        title='Noise vs Fidelity — Quantum Teleportation',
        save_path='results/plots/noise_vs_fidelity.png',
        color='steelblue'
    )

    # --- Plot 2: Shots vs Fidelity ---
    plot_graph(
        x=shot_counts,
        y=fidelities_shots,
        xlabel='Number of Shots',
        ylabel='Fidelity',
        title='Shots vs Fidelity — Quantum Teleportation',
        save_path='results/plots/shots_vs_fidelity.png',
        color='darkorange'
    )

    # --- Plot 3: Theta vs Fidelity ---
    plot_graph(
        x=[round(t, 3) for t in thetas],
        y=fidelities_theta,
        xlabel='Input State Angle Theta (radians)',
        ylabel='Fidelity',
        title='Input State vs Fidelity — Quantum Teleportation',
        save_path='results/plots/theta_vs_fidelity.png',
        color='seagreen'
    )

    print("\nAll experiments done!")
    print("CSV saved to results/data/results.csv")
    print("Plots saved to results/plots/")