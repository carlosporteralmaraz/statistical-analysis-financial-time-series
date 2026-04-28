import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import norm, t

SP = pd.read_csv("trabajo_econofisica/datos/preparados/SP_variables.csv")
UNH = pd.read_csv("trabajo_econofisica/datos/preparados/UNH_variables.csv")

r1_norm_SP = SP["r1_norm"]
r1_UNH = UNH["r1"]
r1_SP = SP["r1"]

#1 S&P500: pdf vs r1_norm
hist, bin_edges = np.histogram(r1_norm_SP, bins=200, density=True)
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
x = np.linspace(-6,6,1200)
df_t, loc_t, scale_t = t.fit(r1_norm_SP)

plt.figure(figsize=(8,5))
plt.scatter(bin_centers, hist, s=10, color="lime", label="S&P500")
plt.ylim(1e-3, 1)
plt.plot(x, norm.pdf(x,0,1), "r", label="Gaussian")
plt.plot(x, t.pdf(x, df_t, loc=loc_t, scale=scale_t), "b--", label="Student")
plt.yscale("log")
plt.xlabel("Normalized S&P500 returns")
plt.ylabel("Probability density")
plt.grid(True)
plt.legend()
plt.savefig("trabajo_econofisica/figures/fat_tails/fig1.png")
plt.show()

#2 UNH: pdf vs r1
hist, bin_edges = np.histogram(r1_UNH, bins=200, density=True)
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
mask = hist > 0
x = np.linspace(-0.068, 0.068,1200)
x2 = np.linspace(-0.1, 0.1, 2000)

df_t, loc_t, scale_t = t.fit(r1_UNH)

plt.figure(figsize=(8,5))
plt.scatter(bin_centers[mask], hist[mask], s=10, label="UNH", color="lime")
plt.plot(x, norm.pdf(x,r1_UNH.mean(), r1_UNH.std()), "r", label="Gaussian")
plt.plot(x2, t.pdf(x2, df_t, loc=loc_t, scale=scale_t), "b--", label="Student")
plt.yscale("log")
plt.xlabel("UNH Log-returns")
plt.ylabel("Probability density function")
plt.grid(True)
plt.ylim(0.05, 46)
plt.legend()
plt.savefig("trabajo_econofisica/figures/fat_tails/fig2.png")
plt.show()


#3.1 
r1_norm_abs_SP = np.abs(r1_norm_SP) 
r_sorted = np.sort(r1_norm_abs_SP)
n = len(r_sorted)
ccdf = 1 - np.arange(1, n+1)/n
mask = r_sorted > 1e-2
plt.figure(figsize=(8,5))
plt.scatter(r_sorted[mask], ccdf[mask], s=5, color="lime", label="S&P500")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Normalized S&P500 returns")
plt.ylabel("Cumulative distribution")
plt.grid(True)
plt.legend()
plt.savefig("trabajo_econofisica/figures/fat_tails/fig3.1.png")
plt.show()

#3 S&P500: ccdf vs r1_norm (poner mask > 0 para ver la figura completa)
r1_norm_abs_SP = np.abs(r1_norm_SP) 
r_sorted = np.sort(r1_norm_abs_SP)
mask = r_sorted > 2.5
n = len(r_sorted)
ccdf = 1 - np.arange(1, n+1)/n
plt.figure(figsize=(8,5))
plt.scatter(r_sorted[mask], ccdf[mask], s=5, color="lime", label="S&P500")
alpha = 3
i0 = 20
x0 = r_sorted[mask][i0]
y0 = ccdf[mask][i0]
C = y0*x0**alpha
x_fit = np.linspace(r_sorted[mask].min(), r_sorted[mask].max(), 300)
y_fit = C * x_fit**(-alpha)
plt.plot(x_fit, y_fit, "r--", label=r"$r^{-3}$")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Normalized S&P500 returns")
plt.ylabel("Cumulative distribution")
plt.grid(True)
plt.legend()
plt.savefig("trabajo_econofisica/figures/fat_tails/fig3.2.png")
plt.show()

#4 S&P500: ccdf vs abs_r1
abs_r1 = SP["abs_r1"]
r_sorted = np.sort(abs_r1)
n = len(r_sorted)
ccdf = 1 - np.arange(1, n+1)/n
mu = r1_SP.mean()
sigma = r1_SP.std()
x = np.linspace(r_sorted.min(), r_sorted.max(), 600)
gauss_ccdf = norm.sf(x, loc=mu, scale=sigma) + norm.cdf(-x, loc=mu, scale=sigma)
df_t, loc_t, scale_t = t.fit(r1_SP)
i0 = int(0.2 * len(r_sorted)) 
x0 = r_sorted[i0]
y0 = ccdf[i0]
y_student_0 = t.sf(x0, df_t, loc=loc_t, scale=scale_t) + t.cdf(-x0, df_t, loc=loc_t, scale=scale_t)
C = y0 / y_student_0
student_ccdf = C*(t.sf(x, df_t, loc=loc_t, scale=scale_t) + t.cdf(-x, df_t, loc=loc_t, scale=scale_t))

plt.figure(figsize=(8,5))
plt.scatter(r_sorted, ccdf, s=5, label="S&P500", color="lime")
plt.plot(x, gauss_ccdf, "r", label="Gaussian")
plt.plot(x, student_ccdf, "b--", label="Student")
plt.xlabel("Absolute S&P500 log-returns")
plt.ylabel("Cumulative distribution")
plt.yscale("log")
plt.ylim(2e-4, 1)
plt.legend()
plt.grid(True)
plt.savefig("trabajo_econofisica/figures/fat_tails/fig4.png")
plt.show()
