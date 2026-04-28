import yfinance as yf
import pandas as pd


SP = yf.download("^GSPC", start = "2000-01-01", end = "2026-01-01").reset_index()
UNH = yf.download("UNH", start = "2000-01-01", end = "2026-01-01").reset_index()

SP.columns = [col[0] if isinstance(col, tuple) else col for col in SP.columns]
UNH.columns = [col[0] if isinstance(col, tuple) else col for col in UNH.columns]

SP.to_csv("trabajo_econofisica/datos/raw/datos_SP_raw.csv", index=False)
UNH.to_csv("trabajo_econofisica/datos/raw/datos_UNH_raw.csv", index=False)

SP["Date"] = pd.to_datetime(SP["Date"])
UNH["Date"] = pd.to_datetime(UNH["Date"])

end_date = SP["Date"].max()

cpi = pd.read_csv("trabajo_econofisica/datos/raw/CPIAUCSL.csv")
cpi = cpi.rename(columns={"observation_date": "Date", "CPIAUCSL" : "CPI"})
cpi["Date"] = pd.to_datetime(cpi["Date"])
cpi = cpi.set_index("Date")
cpi = cpi.asfreq("MS")
cpi = cpi.reindex(pd.date_range(cpi.index.min(), end_date))
cpi = cpi.ffill()
cpi = cpi.reset_index().rename(columns={"index": "Date"})

SP = SP.merge(cpi, on="Date", how="left")
UNH = UNH.merge(cpi, on="Date", how="left")

SP["real_close"] = SP["Close"] / SP["CPI"]
UNH["real_close"] = UNH["Close"] / UNH["CPI"]

print(SP[["Date", "CPI", "real_close"]].isna().sum())
print(UNH[["Date", "CPI", "real_close"]].isna().sum())

SP.to_csv("trabajo_econofisica/datos/preparados/datos_SP.csv", index=False)
UNH.to_csv("trabajo_econofisica/datos/preparados/datos_UNH.csv", index=False)
cpi.to_csv("trabajo_econofisica/datos/preparados/datos_CPI.csv", index=False)



 