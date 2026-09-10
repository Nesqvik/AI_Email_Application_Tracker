import json

SETTINGS = "config/settings.json"


def load_settings():
    with open(SETTINGS) as f:
        return json.load(f)


def save_settings(data):
    with open(SETTINGS, "w") as f:
        json.dump(data, f, indent=4)