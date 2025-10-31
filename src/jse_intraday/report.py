from __future__ import annotations
from .data_loader import load_csv, filter_trading_hours, resample_ohlcv
from .feature_engineering import add_basic_features

def write_summary(csv_path: str, out_path: str = "reports/summary.md") -> None:
    df = load_csv(csv_path)
    df = filter_trading_hours(df)
    df5 = resample_ohlcv(df, "5T")
    feats = add_basic_features(df5)
    period = f"{feats.index.min().date()} to {feats.index.max().date()}"
    avg_ret = feats["log_return"].mean()
    vol = feats["log_return"].std()
    lines = [
        "# JSE Intraday Summary",
        f"- Period: {period}",
        f"- Bars: {len(feats):,}",
        f"- Mean 5-min log return: {avg_ret:.6f}",
        f"- 5-min return std (volatility proxy): {vol:.6f}",
    ]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
