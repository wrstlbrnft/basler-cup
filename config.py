import json


def load_config():
    with open("config.json") as file:
        return json.load(file)
