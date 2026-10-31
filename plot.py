import numpy as np # loads numpy as a short name

data = np.loadtxt("results.csv", delimiter=",", skiprows=1)
# reads csv file, separates columns with commas, skips the header line

t_sim = data[:, 0] / 1000 # column 0: t_thresh -> t
out_sim = data[:, 1] / 1000 #column 1: count -> output

t_fine = np.linspace(0, 1, 200)
f_true = np.sin(np.pi * t_fine)

print(f_true.max())
print(t_sim, out_sim)
