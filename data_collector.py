import random
import time
from database import save_data, init_db

# Generate child IDs C1 to C150
children = [f"C{i}" for i in range(1, 51)]

def generate(child):
    return {
        "child_id": child,
        "heart_rate": random.randint(60,130),
        "temperature": round(random.uniform(36,39),1),
        "steps": random.randint(1000,10000),
        "water_intake": random.randint(500,3000),
        "sleep_hours": round(random.uniform(4,10),1)
    }

def run():
    init_db()

    while True:
        for c in children:
            data = generate(c)
            save_data(data)
            print("Saved:", data)

        time.sleep(5)

if __name__ == "__main__":
    run()