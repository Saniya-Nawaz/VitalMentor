from sklearn.ensemble import IsolationForest

def detect(df):
    model = IsolationForest(contamination=0.1)
    model.fit(df)
    df["anomaly"] = model.predict(df)
    return df