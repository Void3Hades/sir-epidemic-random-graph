"""SIR epidemic on an Erdos-Renyi random graph G(n, c/n).

Outbreak size (fraction ever infected) vs average degree c.
Each infected node infects each susceptible neighbour with probability T,
then recovers after one step. The epidemic threshold is at c * T = 1.
"""
import numpy as np
import matplotlib.pyplot as plt

def er_graph(n, c, rng):
    """Adjacency lists of G(n, p=c/n), sampled edge by edge."""
    m = rng.binomial(n * (n - 1) // 2, c / n)
    u = rng.integers(0, n, m)
    v = rng.integers(0, n, m)
    keep = u != v
    adj = [[] for _ in range(n)]
    for a, b in zip(u[keep], v[keep]):
        adj[a].append(b)
        adj[b].append(a)
    return adj

def sir_outbreak(adj, T, rng):
    """Start from one random node; return fraction of nodes ever infected."""
    n = len(adj)
    state = np.zeros(n, dtype=np.int8)   # 0=S, 1=I, 2=R
    start = rng.integers(n)
    state[start] = 1
    infected = [start]
    total = 1
    while infected:
        new = []
        for i in infected:
            for j in adj[i]:
                if state[j] == 0 and rng.random() < T:
                    state[j] = 1
                    new.append(j)
            state[i] = 2
        total += len(new)
        infected = new
    return total / n

def run(n=2000, T=1.0, runs=100, seed=0):
    rng = np.random.default_rng(seed)
    cs = np.round(np.arange(0.2, 3.01, 0.2), 2)
    means, stds = [], []
    for c in cs:
        sizes = [sir_outbreak(er_graph(n, c, rng), T, rng) for _ in range(runs)]
        means.append(np.mean(sizes)); stds.append(np.std(sizes))
        print(f"c={c:.1f}  mean outbreak={means[-1]:.3f}")
    means, stds = np.array(means), np.array(stds)
    plt.errorbar(cs, means, yerr=stds, marker="o", capsize=3)
    plt.axvline(1 / T, color="r", ls="--", label=f"threshold c = 1/T = {1/T:.2f}")
    plt.xlabel("average degree c"); plt.ylabel("fraction ever infected")
    plt.title(f"SIR on Erdos-Renyi, n={n}, T={T}, {runs} runs per point")
    plt.legend(); plt.savefig(f"sir_er_T{T}.png", dpi=150)

if __name__ == "__main__":
    run(T=0.5)   # then try T=0.5: the jump should move to c = 2