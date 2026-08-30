import json
import os

FILE = "memory.json"

def load_memory():
    if not os.path.exists(FILE):
        return {}
    with open(FILE) as f:
        return json.load(f)

def save_memory(child_id, data):
    mem = load_memory()
    mem[child_id] = data
    with open(FILE, "w") as f:
        json.dump(mem, f, indent=2)