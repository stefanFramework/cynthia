import json
import random

with open("./network_issues.json", "r") as file:
    network_issues = json.load(file)


def run_diagnostics():
    return random.choice(network_issues)
