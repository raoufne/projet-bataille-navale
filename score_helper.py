import os
import json

HIGHSCORE_FILE = "data/highscores.json"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(HIGHSCORE_FILE):
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump({"C": None, "B": None, "A": None, "Z": None}, f)

def load_highscores():
    with open(HIGHSCORE_FILE, "r") as f:
        return json.load(f)

def save_highscores(scores):
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(scores, f, indent=4)