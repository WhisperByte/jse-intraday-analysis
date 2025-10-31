from __future__ import annotations
import pandas as pd
import pytz

REQUIRED_COLS = ["symbol","open","high","low","close","volume"]

def load_csv(path: str, tz: str = "Africa/Johannesburg") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"CSV missing required columns: {missing}")
    df = df.drop_duplicates().sort_values("timestamp").reset_index(drop=True)
    tzinfo = pytz.timezone(tz)
    if df["timestamp"].dt.tz is None:
        df["timestamp"] = df["timestamp"].dt.tz_localize(tzinfo)
    else:
        df["timestamp"] = df["timestamp"].dt.tz_convert(tzinfo)
    df = df.set_index("timestamp")
    for c in ["open","high","low","close","volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["open","high","low","close","volume"])
    return df

def filter_trading_hours(df: pd.DataFrame, start: str = "09:00", end: str = "17:00") -> pd.DataFrame:
    mask = (df.index.time >= pd.to_datetime(start).time()) & (df.index.time <= pd.to_datetime(end).time())
    return df.loc[mask]

def resample_ohlcv(df: pd.DataFrame, rule: str = "5min") -> pd.DataFrame:
    agg = {"open":"first","high":"max","low":"min","close":"last","volume":"sum","symbol":"first"}
    out = df.resample(rule, label="right", closed="right").agg(agg).dropna(subset=["close"])
    return out
