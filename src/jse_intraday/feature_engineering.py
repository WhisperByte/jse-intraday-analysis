import pandas as pd
import numpy as np

def add_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    x["log_return"] = np.log(x["close"] / x["close"].shift(1))
    for w in (5,10,20):
        x[f"roll_mean_{w}"] = x["close"].rolling(w, min_periods=max(1,w//2)).mean()
        x[f"roll_std_{w}"]  = x["close"].rolling(w, min_periods=max(1,w//2)).std()
    x["hour"] = x.index.hour
    x["weekday"] = x.index.dayofweek
    return x.dropna(subset=["log_return"])
