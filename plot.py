import numpy as np # loads numpy as a short name
import matplotlib.pyplot as plt


data = np.loadtxt("results.csv", delimiter=",", skiprows=1)

t_sim = data[:, 0] / 1000 # column 0: t_thresh -> t
out_sim = data[:, 1] / 1000 #column 1: count -> output

t_fine = np.linspace(0, 1, 200) #200 smooth points between 0 & 1
f_true = np.sin(np.pi * t_fine)

plt.plot(t_fine, f_true, label="True sin(πt)") #smooth line
plt.plot(t_sim, out_sim, "o", label= "Stochastic sim (n=4)") #dots

plt.xlabel("t")
plt.ylabel("Output")
plt.title("Bernstein Stochastic Approximation of Sin(πt)")
plt.legend()
plt.savefig("results.png", dpi = 150)
plt.show()