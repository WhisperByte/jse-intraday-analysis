import pandas as pd

def hourly_weekday_pivot(df: pd.DataFrame, value_col: str = "log_return") -> pd.DataFrame:
    if "hour" not in df.columns or "weekday" not in df.columns:
        raise ValueError("Run feature engineering first to add 'hour' and 'weekday'.")
    return df.pivot_table(index="weekday", columns="hour", values=value_col, aggfunc="mean")
