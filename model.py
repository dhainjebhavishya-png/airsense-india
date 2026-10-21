from xgboost import XGBRegressor
from features import add_features
from data import get_data
import pandas as pd


def make_xy(data, h):
    d = data.copy()
    d["target"] = d["pm2_5"].shift(-h)
    d = d.dropna()
    X = d.drop(columns=["pm10", "target"])
    y = d["target"]
    return X, y


def train_model(data, h):
    X, y = make_xy(data, h)
    model = XGBRegressor(n_estimators=300, max_depth=5, learning_rate=0.05, random_state=42)
    model.fit(X, y)
    return model

def train_all(data, horizons=range(1, 25)):
    return {h: train_model(data, h) for h in horizons}


def forecast(models, latest, now):
    rows = []
    for h, m in models.items():
        value = float(m.predict(latest)[0])
        rows.append({"time": now + pd.Timedelta(hours=h), "pm2_5": max(value, 0)})
    return pd.DataFrame(rows).set_index("time")

def latest_row(lat, lon):
    df, source = get_data(lat, lon)
    now = pd.Timestamp.now(tz="Asia/Kolkata").tz_localize(None).floor("h")
    df = df[df.index <= now]
    data = add_features(df)
    row = data.drop(columns=["pm10"]).iloc[[-1]]
    return row, source


if __name__ == "__main__":
    from data import get_long_data

    df = get_long_data(19.07, 72.99)
    data = add_features(df)
    models = train_all(data)

    latest, source = latest_row(19.07, 72.99)
    now = latest.index[0]
    fc = forecast(models, latest, now)
    print(source, "| abhi ka time:", now, "| PM2.5 abhi:", latest["pm2_5"].iloc[0])
    print(fc.head(6))