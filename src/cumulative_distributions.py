import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

SP = pd.read_csv("trabajo_econofisica/datos/preparados/SP_variables.csv")
UNH = pd.read_csv("trabajo_econofisica/datos/preparados/UNH_variables.csv")



#S&P500

r1_norm = SP["r1_norm"]
r5_norm = SP["r5_norm"]
r20_norm = SP["r20_norm"]

r1_sorted = np.sort(r1_norm)
r5_sorted = np.sort(r5_norm)
r20_sorted = np.sort(r20_norm)

n1 = len(r1_sorted)
n5 = len(r5_sorted)
n20 = len(r20_sorted)

ccdf1 = 1 - np.arange(1, n1+1)/n1
ccdf5 = 1 - np.arange(1, n5+1)/n5
ccdf20 = 1 - np.arange(1, n20+1)/n20

plt.figure(figsize=(8,5))
plt.scatter(r1_sorted, ccdf1, s=5, color="red", label="τ = 1 day")
plt.scatter(r5_sorted, ccdf5, s=5, color="lime", label="τ = 1 week")
plt.scatter(r20_sorted, ccdf20, s=5, color="blue", label="τ = 1 month")
x = np.linspace(0, 6, 500)
gauss_ccdf = 2 * norm.sf(x)
plt.plot(x, gauss_ccdf, color="black", label="Gaussian")
plt.yscale("log")
plt.xlabel("Normalized S&P500 returns")
plt.ylabel("Cumulative distribution")
plt.grid(True)
plt.xlim(0, 6)
plt.xticks(np.arange(0, 7, 1))
plt.ylim(1e-3, 1)
print("kurtosis r1 =", r1_norm.kurtosis())
print("kurtosis r5 =", r5_norm.kurtosis())
print("kurtosis r20 =", r20_norm.kurtosis())
plt.legend()
plt.savefig("trabajo_econofisica/figures/cumulative_distributions/figSP.png")
plt.show()

#S&P500
r1_norm = UNH["r1_norm"]
r5_norm = UNH["r5_norm"]
r20_norm = UNH["r20_norm"]

r1_sorted = np.sort(r1_norm)
r5_sorted = np.sort(r5_norm)
r20_sorted = np.sort(r20_norm)

n1 = len(r1_sorted)
n5 = len(r5_sorted)
n20 = len(r20_sorted)

ccdf1 = 1 - np.arange(1, n1+1)/n1
ccdf5 = 1 - np.arange(1, n5+1)/n5
ccdf20 = 1 - np.arange(1, n20+1)/n20

plt.figure(figsize=(8,5))
plt.scatter(r1_sorted, ccdf1, s=5, color="red", label="τ = 1 day")
plt.scatter(r5_sorted, ccdf5, s=5, color="lime", label="τ = 1 week")
plt.scatter(r20_sorted, ccdf20, s=5, color="blue", label="τ = 1 month")
x = np.linspace(0, 6, 500)
gauss_ccdf = 2 * norm.sf(x)
plt.plot(x, gauss_ccdf, color="black", label="Gaussian")
plt.yscale("log")
plt.xlabel("Normalized UNH returns")
plt.ylabel("Cumulative distribution")
plt.grid(True)
plt.xlim(0, 6)
plt.xticks(np.arange(0, 7, 1))
plt.ylim(1e-3, 1)
print("kurtosis r1 =", r1_norm.kurtosis())
print("kurtosis r5 =", r5_norm.kurtosis())
print("kurtosis r20 =", r20_norm.kurtosis())
plt.legend()
plt.savefig("trabajo_econofisica/figures/cumulative_distributions/figUNH.png")
plt.show()