import numpy as np
import pandas as pd

def naive_next_close(df: pd.DataFrame) -> pd.Series:
    return df["close"].shift(1)

def rmse(y_true: pd.Series, y_pred: pd.Series) -> float:
    y = y_true.align(y_pred, join="inner")
    return float(np.sqrt(((y[0] - y[1])**2).mean()))
