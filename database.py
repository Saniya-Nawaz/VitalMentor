import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "data.csv")

def init_db():
    if not os.path.exists(FILE) or os.stat(FILE).st_size == 0:
        df = pd.DataFrame(columns=[
            "child_id","heart_rate","temperature",
            "steps","water_intake","sleep_hours"
        ])
        df.to_csv(FILE, index=False)

def save_data(row):
    df = pd.read_csv(FILE)
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(FILE, index=False)

def load_data():
    if not os.path.exists(FILE) or os.stat(FILE).st_size == 0:
        return pd.DataFrame(columns=[
            "child_id","heart_rate","temperature",
            "steps","water_intake","sleep_hours"
        ])
    return pd.read_csv(FILE)