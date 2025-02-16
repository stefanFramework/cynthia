import os
import json

from dotenv import load_dotenv
from cynthia.integrations.openai.facades import GptFacade
from cynthia.utils import run_diagnostics
from cynthia.ui import launch_chat_interface

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")
gpt = GptFacade(OPENAI_KEY)


def func_tools():
    return [{
        "name": "run_diagnostics",
        "description": "runs a diagnostic of the client network service. " +
                       "Call it every time you need to do a diagnostics test. " +
                       "For instance when a client ask you for help because their network service is not working",
        "parameters": {}
    }]


def handle_tool_call(message):
    diagnostic = run_diagnostics()
    response = {
        "role": "tool",
        "content": diagnostic["diagnostic"]["recommended_action"],
        "tool_call_id": message.tool_calls[0].id
    }
    return response


def chat(text, history):

    result = gpt.get_user_request(text, history, functions=func_tools())

    if result.finish_reason == "tool_calls":
        message = result.message
        function_result = handle_tool_call(message)
        print("--------")
        print(text)
        print("--")
        history.append(function_result)
        print(history)
        print("--")
        result = gpt.get_user_request(text, history)
        return result.message.content

    return result.message.content


launch_chat_interface(chat_function=chat)
