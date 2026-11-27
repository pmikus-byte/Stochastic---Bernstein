"""
Bernstein approximation
For each test function f on [0, 1] compute the Bernstein polynomial B_n f
( this is the value the stochastic circuit converges to) and measure
how close it gets to f as n grows.

Outputs:
  <name>.png: approximation, error vs n, where the error sits
  all_errors.png sup-norm error vs n for every function on one log-log plot
  slopes.csv slopes for every function
"""

import os
import numpy as np
import matplotlib    
matplotlib.use("Agg") # save figures to files
import matplotlib.pyplot as plt
from scipy.stats import binom


#  Bernstein polynomial of f with degree n, evaluated at points x
#    B_n f(x) = sum_i f(i/n) * C(n,i) x^i (1-x)^(n-i)
#    - f(i/n)   the coefficient table (B0..Bn in the hardware)
#    - binom.pmf(...) how often the adder outputs sel = i
#    - .sum(...)  what the output counter averages to

def bernstein(f, n, x):
    i = np.arange(n + 1)
    weights = binom.pmf(i[:, None], n, x)          # shape (n+1, len(x))
    return (f(i / n)[:, None] * weights).sum(axis=0)

functions = {
    "x^2 (sanity)":   lambda t: t**2,
    "tanh(x)":        lambda t: np.tanh(t),
    "sin(pi x)":      lambda t: np.sin(np.pi * t),
    "sin(2 pi x)":    lambda t: np.sin(2 * np.pi * t),
    "|x - 1/2|":      lambda t: np.abs(t - 0.5),
    "sqrt(x)":        lambda t: np.sqrt(t),
    "step at 1/2":    lambda t: np.where(t >= 0.5, 1.0, 0.0),
}

# file names for plots
file_names = {
    "x^2 (sanity)": "x2_sanity",
    "tanh(x)":      "tanh",
    "sin(pi x)":    "sin_pi_x",
    "sin(2 pi x)":  "sin_2pi_x",
    "|x - 1/2|":    "bs_sharp_corner",
    "sqrt(x)":      "sqrt",
    "step at 1/2":  "step",
}

#  Experiment settings
ns = [5, 10, 20, 50, 100, 200, 500, 1000]  # degrees to test
x = np.linspace(0, 1, 10 * max(ns) + 1)  # 10,001 points (>= 10n for every n)
show_ns = [5, 20, 100, 1000]  # which n to draw in the approximation plots

os.makedirs("plots", exist_ok=True)

sup_err = {name: [] for name in functions}
l2_err = {name: [] for name in functions}
approx = {name: {} for name in functions}  # saved B_n f curves for plotting

for n in ns:
    i = np.arange(n + 1)
    weights = binom.pmf(i[:, None], n, x)
    for name, f in functions.items():
        Bn = (f(i / n)[:, None] * weights).sum(axis=0)
        err = np.abs(f(x) - Bn)
        sup_err[name].append(err.max())  # worst error 
        l2_err[name].append(np.sqrt(np.mean(err**2))) # root mean square gap over [0, 1]
        if n in show_ns:
            approx[name][n] = Bn
    print(f"done n = {n}")



# log(error) = slope * log(n) + c
def slope(errors):
    return np.polyfit(np.log(ns), np.log(errors), 1)[0]

rows = []
print()
print(f"{'function':16s} {'sup slope':>10s} {'L2 slope':>10s} {'sup err @ n=1000':>18s}")
for name in functions:
    s_sup, s_l2 = slope(sup_err[name]), slope(l2_err[name])
    rows.append((name, s_sup, s_l2, sup_err[name][-1]))
    print(f"{name:16s} {s_sup:10.2f} {s_l2:10.2f} {sup_err[name][-1]:18.5f}")

with open("plots/slopes.csv", "w") as fh:
    fh.write("function,sup_slope,L2_slope,sup_error_n1000\n")
    for name, s_sup, s_l2, e in rows:
        fh.write(f"{name},{s_sup:.3f},{s_l2:.3f},{e:.6f}\n")


# Plots
for name, f in functions.items():
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))

    #  approximation: f vs B_n f
    ax[0].plot(x, f(x), "k", lw=2, label="f(x)")
    for n in show_ns:
        ax[0].plot(x, approx[name][n], lw=1.2, label=f"B_{n}")
    ax[0].set_title(f"{name}: Bernstein approximations")
    ax[0].set_xlabel("x")
    ax[0].legend(fontsize=8)

    #  error vs n on log-log axes with fitted slopes
    ax[1].loglog(ns, sup_err[name], "o-", label=f"sup error (slope {slope(sup_err[name]):.2f})")
    ax[1].loglog(ns, l2_err[name], "s-", label=f"L2 error (slope {slope(l2_err[name]):.2f})")
    ax[1].set_title("Error vs n")
    ax[1].set_xlabel("n")
    ax[1].set_ylabel("error")
    ax[1].legend(fontsize=8)
    ax[1].grid(True, which="both", alpha=0.3)

    # where  error sits
    for n in [20, 100, 1000]:
        ax[2].plot(x, np.abs(f(x) - approx[name][n] if n in approx[name]
                             else f(x) - bernstein(f, n, x)), lw=1, label=f"n = {n}")
    ax[2].set_title("Where the error sits: |f - B_n f|")
    ax[2].set_xlabel("x")
    ax[2].set_yscale("log")
    ax[2].legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(f"plots/{file_names[name]}.png", dpi=150)
    plt.close(fig)

# summary
fig, ax = plt.subplots(figsize=(7, 5))
for name in functions:
    ax.loglog(ns, sup_err[name], "o-", label=f"{name} ({slope(sup_err[name]):.2f})")
ax.set_title("Sup-norm error vs n (slope in legend)")
ax.set_xlabel("n")
ax.set_ylabel("sup error")
ax.grid(True, which="both", alpha=0.3)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig("plots/all_errors.png", dpi=150)
plt.close(fig)

print("\nSaved plots to the plots/ folder.")