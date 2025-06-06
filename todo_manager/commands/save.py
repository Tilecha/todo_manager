import json
from commands.load import DATA_PATH

def save_tasks(memory):
    with open(DATA_PATH, "w") as f:
            json.dump(memory,f,ensure_ascii=False, indent=2)