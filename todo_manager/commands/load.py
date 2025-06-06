import os
import json

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")    

def load_tasks():

    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:

            try:

                return json.load(f)
            
            except json.JSONDecodeError:
                return []
            
    return []