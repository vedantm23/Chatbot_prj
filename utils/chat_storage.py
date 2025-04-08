import json
import os

def save_chat(question, response, path="chat_history.json"):
    chat_data = {"question": question, "response": response}
    if os.path.exists(path):
        with open(path, "r") as file:
            history = json.load(file)
    else:
        history = []

    history.append(chat_data)

    with open(path, "w") as file:
        json.dump(history, file, indent=4)

def load_chat(path="chat_history.json"):
    if os.path.exists(path):
        with open(path, "r") as file:
            return json.load(file)
    return []
