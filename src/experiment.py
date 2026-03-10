# src/experiment.py
# Sweeps parameters and records fidelity data

import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.circuit import create_teleportation_circuit
from src.simulator import run_qasm, run_with_noise
from src.utils import compute_fidelity, save_results

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

    # --- Save all results to CSV ---
    save_results(
        {'noise_level': noise_levels, 'fidelity_noise': fidelities_noise},
        'results/data/noise_results.csv'
    )
    save_results(
        {'shots': shot_counts, 'fidelity_shots': fidelities_shots},
        'results/data/shots_results.csv'
    )
    save_results(
        {'theta': [round(t, 4) for t in thetas], 'fidelity_theta': fidelities_theta},
        'results/data/theta_results.csv'
    )

    # --- Generate beautiful plots ---
    from src.utils import plot_noise_vs_fidelity, plot_shots_vs_fidelity, plot_theta_vs_fidelity

    plot_noise_vs_fidelity(noise_levels, fidelities_noise,
                           'results/plots/noise_vs_fidelity.png')
    plot_shots_vs_fidelity(shot_counts, fidelities_shots,
                           'results/plots/shots_vs_fidelity.png')
    plot_theta_vs_fidelity(thetas, fidelities_theta,
                           'results/plots/theta_vs_fidelity.png')

    print("\nAll experiments done!")
    print("CSVs saved to results/data/")
    print("Plots saved to results/plots/")
