import json
import random

with open("./network_issues.json", "r") as file:
    network_issues = json.load(file)


def run_diagnostics():
    return random.choice(network_issues)


def func_tools():
    return [{
        "name": "run_diagnostics",
        "description": "runs a diagnostic of the client network service. " +
                       "Call it every time you need to do a diagnostics test. " +
                       "For instance when a client ask you for help because their network service is not working",
        "parameters": {}
    }]


def handle_tool_call(message):
    message_tool_calls = message.tool_calls
    message_function_data = message_tool_calls[0].function

    if message_function_data.name == "run_diagnostics":
        diagnostic = run_diagnostics()
        return {
            "role": "tool",
            "content": diagnostic["diagnostic"]["recommended_action"],
            "tool_call_id": message.tool_calls[0].id
        }

    return {}
