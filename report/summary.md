# Experiment Summary — Quantum Teleportation Fidelity

## Objective

I wanted to go beyond just implementing the teleportation circuit and
actually quantify its performance. Specifically — how does it hold up
under noise? Does it work for all input states? And how many shots do
you actually need before your results are trustworthy?

## Methodology

### Circuit Design

The circuit uses three qubits. Alice prepares her payload qubit in a
known state using an Ry(θ) rotation, so I can calculate exactly what
the output should be and measure fidelity against that. She and Bob
share a Bell pair, which acts as the quantum channel.

Alice measures her two qubits and the results get stored as classical
bits. Bob reads those bits and applies conditional X and Z corrections
to his qubit. After correction, his qubit should be in exactly the
state Alice started with.

### Fidelity Calculation

I calculated fidelity as:
```
F = 1 - |P_measured(|1⟩) - P_theoretical(|1⟩)|
```

For a state prepared with Ry(θ), the theoretical probability of
measuring |1⟩ is sin²(θ/2). Comparing Bob's measured probability
against this gives a clean fidelity score between 0 and 1.

### Noise Model

I used Qiskit Aer's depolarizing noise model — single-qubit gate
errors at rate p, and two-qubit (CNOT) gate errors at rate 2p, since
two-qubit gates are consistently harder to execute cleanly on real
hardware.

## Observations

### Experiment 1 — Noise vs Fidelity

| Noise Level | Fidelity |
|---|---|
| 0.00 | 0.9968 |
| 0.02 | 0.9751 |
| 0.04 | 0.9419 |
| 0.06 | 0.9174 |
| 0.08 | 0.9064 |
| 0.10 | 0.8875 |
| 0.15 | 0.8359 |
| 0.20 | 0.8192 |
| 0.25 | 0.7867 |
| 0.30 | 0.7725 |

The drop is sharpest in the 0–6% range, then starts to flatten. My
guess is that once noise is high enough, the circuit is already
producing near-random outputs, so additional noise doesn't change
much. The 0.776 figure at 30% noise is close to the classical fidelity
limit of 2/3 — a useful benchmark for when teleportation stops being
worth it.

### Experiment 2 — Shots vs Fidelity

Low shot counts produce noisy, unreliable fidelity estimates. At 64
shots I got values jumping between 0.90 and 1.00 across runs. Above
512 shots the estimates stabilize consistently near the true value.
For any serious experiment I'd set a minimum of 1024 shots.

### Experiment 3 — Theta vs Fidelity

Fidelity stayed above 0.97 across all 12 angles I tested. The circuit
doesn't have a "sweet spot" — it performs consistently regardless of
the input state. This is important because a real use case would
involve arbitrary unknown states, not just convenient ones.

## Key Insight

The teleportation protocol itself is robust. What isn't robust is the
physical implementation. Gate errors compound across the circuit's
depth, and even 2% depolarizing noise produces a measurable fidelity
drop. This is why error correction is the central unsolved problem in
quantum computing — not algorithm design.

## Limitations

- This is a simulation, not real hardware. Real devices have correlated errors,
  crosstalk, and drift that depolarizing noise doesn't capture.
- Fidelity metric assumes state preparation is perfect.
- Only single-qubit teleportation — multi-qubit extension would be a more demanding test.

## What I'd Do Next

- Run this on an actual IBM quantum device and compare against
  simulation results
- Try Zero Noise Extrapolation to see if fidelity can be recovered
  post-measurement
- Test different noise models — thermal relaxation and amplitude
  damping are more physically realistic
- Extend to teleporting a 2-qubit entangled state