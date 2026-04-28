import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

SP = pd.read_csv("trabajo_econofisica/datos/preparados/SP_variables.csv")
UNH = pd.read_csv("trabajo_econofisica/datos/preparados/UNH_variables.csv")

def autocorr_values(series, max_lag):
    series = series.dropna()
    return [series.autocorr(lag=k) for k in range(1, max_lag + 1)]

def plot_acf(series, label, title, output_path, max_lag=90, show_conf=True):
    acf = autocorr_values(series, max_lag)
    lags = np.arange(1, max_lag + 1)

    plt.figure(figsize=(8, 5))
    plt.plot(lags, acf, marker="o", linestyle="-", label=label, color="red", alpha=0.5)
    plt.axhline(0, color="black", linewidth=1)

    if show_conf:
        N = series.dropna().shape[0]
        conf = 1.96 / np.sqrt(N)
        plt.axhline(conf, linestyle="--", color="black")
        plt.axhline(-conf, linestyle="--", color="black")

    plt.xlabel("Lag (days)")
    plt.ylabel("Autocorrelation")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.show()

max_lag = 90

plot_acf(
    SP["r1"],
    label="S&P500 r1",
    title="Autocorrelación de retornos diarios - S&P500",
    output_path="trabajo_econofisica/figures/correlation/SP1.png",
    max_lag=max_lag,
    show_conf=True
)

plot_acf(
    SP["abs_r1"],
    label="S&P500 abs(r1)",
    title="Autocorrelación de retornos absolutos diarios - S&P500",
    output_path="trabajo_econofisica/figures/correlation/SP2.png",
    max_lag=max_lag,
    show_conf=False
)

plot_acf(
    UNH["r1"],
    label="UNH r1",
    title="Autocorrelación de retornos diarios - UNH",
    output_path="trabajo_econofisica/figures/correlation/UNH1.png",
    max_lag=max_lag,
    show_conf=True
)

plot_acf(
    UNH["abs_r1"],
    label="UNH abs(r1)",
    title="Autocorrelación de retornos absolutos diarios - UNH",
    output_path="trabajo_econofisica/figures/correlation/UNH2.png",
    max_lag=max_lag,
    show_conf=False
)