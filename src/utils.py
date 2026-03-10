# src/utils.py
# Helpers for fidelity, plotting, saving

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


def compute_fidelity(counts, theta, shots=None):
    """
    Fidelity = 1 - |measured_prob - theoretical_prob|
    
    Bob's bit is the FIRST character in each key e.g. '1 01'
    theoretical_prob = sin(theta/2)^2
    """
    total = sum(counts.values())
    bob_ones = sum(v for k, v in counts.items() if k.strip()[0] == '1')
    measured_prob = bob_ones / total
    theoretical_prob = np.sin(theta / 2) ** 2
    fidelity = 1 - abs(measured_prob - theoretical_prob)
    return round(fidelity, 4)
def plot_noise_vs_fidelity(noise_levels, fidelities, save_path):
    """Publication quality noise vs fidelity plot."""
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(noise_levels, fidelities, marker='o', color='steelblue',
            linewidth=2.5, markersize=8, label='Simulated Fidelity')

    # Shade the "acceptable" fidelity zone
    ax.axhspan(0.9, 1.0, alpha=0.08, color='green', label='High Fidelity Zone (>0.9)')
    ax.axhspan(0.0, 0.9, alpha=0.08, color='red', label='Degraded Zone (<0.9)')
    ax.axhline(y=0.9, color='gray', linestyle='--', linewidth=1, alpha=0.7)

    ax.set_xlabel('Depolarizing Noise Level', fontsize=13)
    ax.set_ylabel('Teleportation Fidelity', fontsize=13)
    ax.set_title('Effect of Noise on Quantum Teleportation Fidelity', fontsize=15, fontweight='bold')
    ax.set_ylim(0.5, 1.05)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    # Annotate key points
    ax.annotate(f'Ideal: {fidelities[0]:.4f}',
                xy=(noise_levels[0], fidelities[0]),
                xytext=(0.02, fidelities[0] - 0.04),
                fontsize=9, color='green',
                arrowprops=dict(arrowstyle='->', color='green', lw=1.2))

    ax.annotate(f'Max Noise: {fidelities[-1]:.4f}',
                xy=(noise_levels[-1], fidelities[-1]),
                xytext=(noise_levels[-1] - 0.08, fidelities[-1] - 0.05),
                fontsize=9, color='red',
                arrowprops=dict(arrowstyle='->', color='red', lw=1.2))

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Plot saved to {save_path}")


def plot_shots_vs_fidelity(shot_counts, fidelities, save_path):
    """Publication quality shots vs fidelity plot."""
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(shot_counts, fidelities, marker='s', color='darkorange',
            linewidth=2.5, markersize=8, label='Measured Fidelity')
    ax.axhline(y=fidelities[-1], color='gray', linestyle='--',
               linewidth=1.2, alpha=0.7, label=f'Converged value ≈ {fidelities[-1]:.4f}')

    ax.set_xscale('log')
    ax.set_xlabel('Number of Shots (log scale)', fontsize=13)
    ax.set_ylabel('Teleportation Fidelity', fontsize=13)
    ax.set_title('Statistical Convergence: Shots vs Fidelity', fontsize=15, fontweight='bold')
    ax.set_ylim(0.7, 1.05)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Plot saved to {save_path}")


def plot_theta_vs_fidelity(thetas, fidelities, save_path):
    """Publication quality theta vs fidelity plot."""
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(thetas, fidelities, marker='^', color='seagreen',
            linewidth=2.5, markersize=8, label='Measured Fidelity')
    ax.axhline(y=1.0, color='gray', linestyle='--',
               linewidth=1.2, alpha=0.7, label='Perfect Fidelity = 1.0')

    # Mark pi/2 and pi
    ax.axvline(x=np.pi/2, color='purple', linestyle=':', alpha=0.6, label='θ = π/2')
    ax.axvline(x=np.pi,   color='brown',  linestyle=':', alpha=0.6, label='θ = π')

    ax.set_xlabel('Input State Angle θ (radians)', fontsize=13)
    ax.set_ylabel('Teleportation Fidelity', fontsize=13)
    ax.set_title('Fidelity Across Different Input States', fontsize=15, fontweight='bold')
    ax.set_ylim(0.9, 1.02)
    ax.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
    ax.set_xticklabels(['0', 'π/4', 'π/2', '3π/4', 'π'])
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Plot saved to {save_path}")


def save_results(data_dict, filepath):
    """Saves a dict of lists to CSV."""
    df = pd.DataFrame(data_dict)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Results saved to {filepath}")

def save_results(data_dict, filepath):
    """Saves a dict of lists to CSV."""
    df = pd.DataFrame(data_dict)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Results saved to {filepath}")