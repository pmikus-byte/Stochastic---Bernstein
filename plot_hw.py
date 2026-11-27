import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

runs = {
    "tanh(x)":           ("tanh.csv",  [0, 251, 473, 650, 780],    lambda t: np.tanh(t)),
    "|x - 1/2|":         ("abs.csv",   [512, 256, 0, 256, 512],    lambda t: np.abs(t - 0.5)),
    "sqrt(x)":           ("sqrt.csv",  [0, 512, 724, 887, 1024],   lambda t: np.sqrt(t)),
    "(1 + sin 2pi x)/2": ("sin2.csv",  [512, 1024, 512, 0, 512],   lambda t: (1 + np.sin(2*np.pi*t)) / 2),
    "step at 1/2":       ("step.csv",  [0, 0, 1024, 1024, 1024],   lambda t: np.where(t >= 0.5, 1.0, 0.0)),
}

def exact_b4(B, t):
    b = np.array(B) / 1024
    i = np.arange(5)
    return (b[:, None] * binom.pmf(i[:, None], 4, t)).sum(axis=0)

x = np.linspace(0, 1, 501)
fig, axes = plt.subplots(1, len(runs), figsize=(20, 3.8), sharey=True)

for ax, (name, (fname, B, f)) in zip(axes, runs.items()):
    with open("hw_results/" + fname) as fh:
        rows = list(csv.DictReader(fh))
    t  = np.array([int(r["t_thresh"]) for r in rows]) / 1024
    hw = np.array([int(r["count"]) for r in rows]) / 1024

    noise = np.abs(hw - exact_b4(B, t)).max()
    print(f"{name:20s} max |hardware - exact B4| = {noise:.4f}")

    ax.plot(x, f(x), "k", lw=2, label="f(x)")
    ax.plot(x, exact_b4(B, x), "--", label="exact B4")
    ax.plot(t, hw, "s", ms=5, label="hardware")
    ax.set_title(name)
    ax.set_xlabel("t")

axes[0].legend(fontsize=8)
fig.tight_layout()
fig.savefig("plots/hw_functions.png", dpi=150)
print("saved plots/hw_functions.png")