# SIR epidemic on Erdős–Rényi random graphs

Simulates an SIR epidemic on G(n, c/n) and measures the fraction of nodes
ever infected as the average degree c varies. The outbreak threshold is
at c·T = 1, where T is the transmission probability.

Run: `python3 sir_er.py` (needs numpy and matplotlib).
Plots: `sir_er_T1.0.png`, `sir_er_T0.5.png`