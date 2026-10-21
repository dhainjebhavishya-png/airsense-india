from data import get_data


def add_features(df):
    df = df.copy()
    df["hour"] = df.index.hour
    df["dayofweek"] = df.index.dayofweek
    df["pm_lag1"] = df["pm2_5"].shift(1)
    df["pm_lag24"] = df["pm2_5"].shift(24)
    df["pm_lag3"] = df["pm2_5"].shift(3)
    df["pm_mean6"] = df["pm2_5"].shift(1).rolling(6).mean()
    df["is_rush"] = df["hour"].isin([8, 9, 10, 17, 18, 19, 20]).astype(int)
    return df.dropna()


if __name__ == "__main__":
    df, source = get_data(19.07, 72.99)
    f = add_features(df)
    print(f.tail())
    print(f.shape)