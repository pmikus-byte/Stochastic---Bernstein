import numpy as np # loads numpy as a short name
import matplotlib.pyplot as plt
from math import comb

t_fine = np.linspace(0, 1, 200) #200 points between 0 & 1
f_true = np.sin(np.pi * t_fine)

# hardware results
hw = np.loadtxt("results/rtl_sin.csv", delimiter=",", skiprows=1)
t_hw = hw[:, 0] / 1024
out_hw = hw[:, 1] / 1024

# exact Bernstein curve (n = 4)
n = 4
b = np.array([0, 724, 1024, 724, 0]) / 1024
f_bern = sum(b[i] * comb(n, i) * t_fine**i * (1 - t_fine)**(n - i) for i in range(n + 1))

data = np.loadtxt("results/behavioral_sin.csv", delimiter=",", skiprows=1)

t_sim = data[:, 0] / 1000 # column 0: t_thresh -> t
out_sim = data[:, 1] / 1000 #column 1: count -> output

plt.plot(t_fine, f_true, label="True sin(πt)") #line
plt.plot(t_sim, out_sim, "o", label= r"Behavioral sim (\$urandom)") #dots
plt.plot(t_fine, f_bern, "--", label="Exact Bernstein (n=4)")
plt.plot(t_hw, out_hw, "s", label="Hardware RTL sim (LFSR)") # "s" = square markers

plt.xlabel("t")
plt.ylabel("Output")
plt.title("Bernstein Stochastic Approximation of Sin(πt)")
plt.legend()
plt.savefig("plots/sin_comparison.png", dpi = 150)
plt.show()