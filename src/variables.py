import numpy as np
import pandas as pd

SP = pd.read_csv("trabajo_econofisica/datos/preparados/datos_SP.csv")
UNH = pd.read_csv("trabajo_econofisica/datos/preparados/datos_UNH.csv")

SP["Date"] = pd.to_datetime(SP["Date"])
UNH["Date"] = pd.to_datetime(UNH["Date"])

def build_variables(df):
    df = df.copy()

    # Retornos diarios: se mantienen todos los días
    df["r1"] = np.log(df["real_close"] / df["real_close"].shift(1))
    df["abs_r1"] = np.abs(df["r1"])
    df["r1_2"] = df["r1"]**2
    df["r1_norm"] = (df["r1"] - df["r1"].mean()) / df["r1"].std()

    # Dataset diario para fat tails y autocorrelación
    df_daily = df.dropna(subset=["r1", "abs_r1", "r1_2", "r1_norm"]).copy()

    # Retornos no solapados para aggregational normality
    prices = df["real_close"].dropna().reset_index(drop=True)

    r1 = np.log(prices / prices.shift(1)).dropna()
    r5 = np.log(prices / prices.shift(5)).dropna()[::5]
    r20 = np.log(prices / prices.shift(20)).dropna()[::20]

    r1_norm = (r1 - r1.mean()) / r1.std()
    r5_norm = (r5 - r5.mean()) / r5.std()
    r20_norm = (r20 - r20.mean()) / r20.std()

    df_tau = pd.DataFrame({
        "r1_norm": r1_norm.reset_index(drop=True),
        "r5_norm": r5_norm.reset_index(drop=True),
        "r20_norm": r20_norm.reset_index(drop=True)
    })

    return df_daily, df_tau

SP_daily, SP_tau = build_variables(SP)
UNH_daily, UNH_tau = build_variables(UNH)

SP_daily.to_csv("trabajo_econofisica/datos/preparados/SP_variables.csv", index=False)
UNH_daily.to_csv("trabajo_econofisica/datos/preparados/UNH_variables.csv", index=False)

SP_tau.to_csv("trabajo_econofisica/datos/preparados/SP_tau_variables.csv", index=False)
UNH_tau.to_csv("trabajo_econofisica/datos/preparados/UNH_tau_variables.csv", index=False)