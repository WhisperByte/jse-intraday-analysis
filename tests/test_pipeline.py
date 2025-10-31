from jse_intraday.data_loader import load_csv, filter_trading_hours, resample_ohlcv
from jse_intraday.feature_engineering import add_basic_features
from jse_intraday.seasonality import hourly_weekday_pivot

def test_pipeline():
    df = load_csv("data/raw/sample_AGL.csv")
    df = filter_trading_hours(df)
    df5 = resample_ohlcv(df, "5T")
    feats = add_basic_features(df5)
    piv = hourly_weekday_pivot(feats)
    assert piv.shape[0] <= 7 and feats.shape[0] > 0
