import json
from typing import Any
from cynthia.integrations.openai.clients import GptClient


class GptFacade:
    def __init__(self, api_key: str):
        self.client = GptClient(api_key=api_key)

    def get_user_request(
            self,
            user_request: str,
            history: list[dict[str, Any]] = None,
            functions: list[dict[str, Any]] = None
    ):
        messages = self._build_messages_parameter(user_request, history)
        tools = self._build_tools_parameter(functions)
        return self.client.execute_completion(
            messages=messages,
            tools=tools
        )

    def _build_messages_parameter(
            self,
            user_request: str,
            history: list[dict[str, Any]] = None
    ):
        system_message = {
            "role": "system",
            "content": "You are a Technical support assistant." +
                       " Your mission is to provide a diagnostic to a customer. " +
                       "You have to be kind and make clear and short explanations"
        }

        messages = [system_message]

        if history:
            messages += history

        user_message = {
            "role": "user",
            "content": user_request  # f"{user_request}. The output format must be JSON "
        }

        messages.append(user_message)

        return messages

    def _build_tools_parameter(self, functions: list[dict[str, Any]] = None):
        if not functions:
            return None

        return [{"type": "function", "function": f} for f in functions]
