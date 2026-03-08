# src/utils.py
# Helpers for fidelity, plotting, saving

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


def compute_fidelity(counts, theta, shots=1024):
    """
    Correct fidelity calculation.
    
    For state Ry(theta)|0>, the probability of measuring |1> = sin(theta/2)^2
    We compare Bob's measured |1> probability vs the theoretical value.
    Fidelity = 1 - |measured_prob - theoretical_prob|
    """
    total = sum(counts.values())
    
    # Bob's bit is the FIRST character in each key
    bob_ones = sum(v for k, v in counts.items() if k.strip().split(' ')[0] == '1')
    measured_prob = bob_ones / total
    
    # What probability SHOULD we see given theta?
    theoretical_prob = np.sin(theta / 2) ** 2
    
    fidelity = 1 - abs(measured_prob - theoretical_prob)
    return round(fidelity, 4)

def plot_graph(x, y, xlabel, ylabel, title, save_path, color='steelblue'):
    """Plots and saves a line graph."""
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, marker='o', color=color, linewidth=2, markersize=5)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14)
    plt.grid(True, alpha=0.3)
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