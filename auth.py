import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "users.json")


if not os.path.exists(file_path):
    default_users = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },

    "parent1": {"password": "parent123", "role": "parent", "child_id": "C1"},
    "child1": {"password": "child123", "role": "child", "child_id": "C1"},

    "parent2": {"password": "parent123", "role": "parent", "child_id": "C2"},
    "child2": {"password": "child123", "role": "child", "child_id": "C2"},

    "parent3": {"password": "parent123", "role": "parent", "child_id": "C3"},
    "child3": {"password": "child123", "role": "child", "child_id": "C3"},

    "parent4": {"password": "parent123", "role": "parent", "child_id": "C4"},
    "child4": {"password": "child123", "role": "child", "child_id": "C4"},

    "parent5": {"password": "parent123", "role": "parent", "child_id": "C5"},
    "child5": {"password": "child123", "role": "child", "child_id": "C5"},

    "parent6": {"password": "parent123", "role": "parent", "child_id": "C6"},
    "child6": {"password": "child123", "role": "child", "child_id": "C6"},

    "parent7": {"password": "parent123", "role": "parent", "child_id": "C7"},
    "child7": {"password": "child123", "role": "child", "child_id": "C7"},

    "parent8": {"password": "parent123", "role": "parent", "child_id": "C8"},
    "child8": {"password": "child123", "role": "child", "child_id": "C8"},

    "parent9": {"password": "parent123", "role": "parent", "child_id": "C9"},
    "child9": {"password": "child123", "role": "child", "child_id": "C9"},

    "parent10": {"password": "parent123", "role": "parent", "child_id": "C10"},
    "child10": {"password": "child123", "role": "child", "child_id": "C10"},

    "parent11": {"password": "parent123", "role": "parent", "child_id": "C11"},
    "child11": {"password": "child123", "role": "child", "child_id": "C11"},

    "parent12": {"password": "parent123", "role": "parent", "child_id": "C12"},
    "child12": {"password": "child123", "role": "child", "child_id": "C12"},

    "parent13": {"password": "parent123", "role": "parent", "child_id": "C13"},
    "child13": {"password": "child123", "role": "child", "child_id": "C13"},

    "parent14": {"password": "parent123", "role": "parent", "child_id": "C14"},
    "child14": {"password": "child123", "role": "child", "child_id": "C14"},

    "parent15": {"password": "parent123", "role": "parent", "child_id": "C15"},
    "child15": {"password": "child123", "role": "child", "child_id": "C15"},

    "parent16": {"password": "parent123", "role": "parent", "child_id": "C16"},
    "child16": {"password": "child123", "role": "child", "child_id": "C16"},

    "parent17": {"password": "parent123", "role": "parent", "child_id": "C17"},
    "child17": {"password": "child123", "role": "child", "child_id": "C17"},

    "parent18": {"password": "parent123", "role": "parent", "child_id": "C18"},
    "child18": {"password": "child123", "role": "child", "child_id": "C18"},

    "parent19": {"password": "parent123", "role": "parent", "child_id": "C19"},
    "child19": {"password": "child123", "role": "child", "child_id": "C19"},

    "parent20": {"password": "parent123", "role": "parent", "child_id": "C20"},
    "child20": {"password": "child123", "role": "child", "child_id": "C20"},

    "parent21": {"password": "parent123", "role": "parent", "child_id": "C21"},
    "child21": {"password": "child123", "role": "child", "child_id": "C21"},

    "parent22": {"password": "parent123", "role": "parent", "child_id": "C22"},
    "child22": {"password": "child123", "role": "child", "child_id": "C22"},

    "parent23": {"password": "parent123", "role": "parent", "child_id": "C23"},
    "child23": {"password": "child123", "role": "child", "child_id": "C23"},

    "parent24": {"password": "parent123", "role": "parent", "child_id": "C24"},
    "child24": {"password": "child123", "role": "child", "child_id": "C24"},

    "parent25": {"password": "parent123", "role": "parent", "child_id": "C25"},
    "child25": {"password": "child123", "role": "child", "child_id": "C25"},

    "parent26": {"password": "parent123", "role": "parent", "child_id": "C26"},
    "child26": {"password": "child123", "role": "child", "child_id": "C26"},

    "parent27": {"password": "parent123", "role": "parent", "child_id": "C27"},
    "child27": {"password": "child123", "role": "child", "child_id": "C27"},

    "parent28": {"password": "parent123", "role": "parent", "child_id": "C28"},
    "child28": {"password": "child123", "role": "child", "child_id": "C28"},

    "parent29": {"password": "parent123", "role": "parent", "child_id": "C29"},
    "child29": {"password": "child123", "role": "child", "child_id": "C29"},

    "parent30": {"password": "parent123", "role": "parent", "child_id": "C30"},
    "child30": {"password": "child123", "role": "child", "child_id": "C30"},

    "parent31": {"password": "parent123", "role": "parent", "child_id": "C31"},
    "child31": {"password": "child123", "role": "child", "child_id": "C31"},

    "parent32": {"password": "parent123", "role": "parent", "child_id": "C32"},
    "child32": {"password": "child123", "role": "child", "child_id": "C32"},

    "parent33": {"password": "parent123", "role": "parent", "child_id": "C33"},
    "child33": {"password": "child123", "role": "child", "child_id": "C33"},

    "parent34": {"password": "parent123", "role": "parent", "child_id": "C34"},
    "child34": {"password": "child123", "role": "child", "child_id": "C34"},

    "parent35": {"password": "parent123", "role": "parent", "child_id": "C35"},
    "child35": {"password": "child123", "role": "child", "child_id": "C35"},

    "parent36": {"password": "parent123", "role": "parent", "child_id": "C36"},
    "child36": {"password": "child123", "role": "child", "child_id": "C36"},

    "parent37": {"password": "parent123", "role": "parent", "child_id": "C37"},
    "child37": {"password": "child123", "role": "child", "child_id": "C37"},

    "parent38": {"password": "parent123", "role": "parent", "child_id": "C38"},
    "child38": {"password": "child123", "role": "child", "child_id": "C38"},

    "parent39": {"password": "parent123", "role": "parent", "child_id": "C39"},
    "child39": {"password": "child123", "role": "child", "child_id": "C39"},

    "parent40": {"password": "parent123", "role": "parent", "child_id": "C40"},
    "child40": {"password": "child123", "role": "child", "child_id": "C40"},

    "parent41": {"password": "parent123", "role": "parent", "child_id": "C41"},
    "child41": {"password": "child123", "role": "child", "child_id": "C41"},

    "parent42": {"password": "parent123", "role": "parent", "child_id": "C42"},
    "child42": {"password": "child123", "role": "child", "child_id": "C42"},

    "parent43": {"password": "parent123", "role": "parent", "child_id": "C43"},
    "child43": {"password": "child123", "role": "child", "child_id": "C43"},

    "parent44": {"password": "parent123", "role": "parent", "child_id": "C44"},
    "child44": {"password": "child123", "role": "child", "child_id": "C44"},

    "parent45": {"password": "parent123", "role": "parent", "child_id": "C45"},
    "child45": {"password": "child123", "role": "child", "child_id": "C45"},

    "parent46": {"password": "parent123", "role": "parent", "child_id": "C46"},
    "child46": {"password": "child123", "role": "child", "child_id": "C46"},

    "parent47": {"password": "parent123", "role": "parent", "child_id": "C47"},
    "child47": {"password": "child123", "role": "child", "child_id": "C47"},

    "parent48": {"password": "parent123", "role": "parent", "child_id": "C48"},
    "child48": {"password": "child123", "role": "child", "child_id": "C48"},

    "parent49": {"password": "parent123", "role": "parent", "child_id": "C49"},
    "child49": {"password": "child123", "role": "child", "child_id": "C49"},

    "parent50": {"password": "parent123", "role": "parent", "child_id": "C50"},
    "child50": {"password": "child123", "role": "child", "child_id": "C50"}
    }
    with open(file_path, "w") as f:
        json.dump(default_users, f, indent=4)

with open(file_path) as f:
    users = json.load(f)

def login(username, password):
    if username in users and users[username]["password"] == password:
        return users[username]
    return None