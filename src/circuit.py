# src/circuit.py
# Builds the quantum teleportation circuit

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import numpy as np


def create_teleportation_circuit(state_angle_theta=None, state_angle_phi=None):
    """
    Builds a 3-qubit quantum teleportation circuit.

    Qubits:
        q0 = Alice's payload qubit (the state to teleport)
        q1 = Alice's half of the Bell pair
        q2 = Bob's half of the Bell pair

    Classical bits:
        alice_bits = Alice's 2 measurement results
        bob_bit    = Bob's final measurement
    """

    if state_angle_theta is None:
        state_angle_theta = np.random.uniform(0, np.pi)
    if state_angle_phi is None:
        state_angle_phi = 0.0

    # Define registers
    qr = QuantumRegister(3, name='q')
    cr_alice = ClassicalRegister(2, name='alice_bits')
    cr_bob   = ClassicalRegister(1, name='bob_bit')

    qc = QuantumCircuit(qr, cr_alice, cr_bob)

    # Step 1: Prepare Alice's qubit in a known state
    qc.ry(state_angle_theta, qr[0])
    qc.rz(state_angle_phi, qr[0])
    qc.barrier(label='State Prep')

    # Step 2: Create Bell pair between q1 and q2
    qc.h(qr[1])
    qc.cx(qr[1], qr[2])
    qc.barrier(label='Bell Pair')

    # Step 3: Alice entangles her payload with her Bell qubit
    qc.cx(qr[0], qr[1])
    qc.h(qr[0])
    qc.barrier(label="Alice Ops")

    # Step 4: Alice measures and result stored in classical bits
    qc.measure(qr[0], cr_alice[0])
    qc.measure(qr[1], cr_alice[1])
    qc.barrier(label='Measurement')

    # Step 5: Bob applies corrections based on Alice's bits
    with qc.if_test((cr_alice[1], 1)):
        qc.x(qr[2])
    with qc.if_test((cr_alice[0], 1)):
        qc.z(qr[2])

    # Step 6: Bob measures his qubit
    qc.measure(qr[2], cr_bob[0])

    expected_state = {
        'theta': state_angle_theta,
        'phi': state_angle_phi
    }

    return qc, expected_state


def draw_circuit(qc, save_path='images/circuit.png'):
    """Saves circuit diagram as PNG."""
    fig = qc.draw(output='mpl', fold=-1)
    fig.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Circuit saved to {save_path}")


if __name__ == "__main__":
    qc, state_info = create_teleportation_circuit(state_angle_theta=np.pi/3)
    print("Circuit created successfully!")
    print(f"Angles: theta={state_info['theta']:.4f}, phi={state_info['phi']:.4f}")
    print(f"Depth: {qc.depth()}")
    print(f"Gates: {qc.count_ops()}")
    draw_circuit(qc)
    print(qc.draw(output='text'))