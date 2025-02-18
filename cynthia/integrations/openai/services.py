import json
from typing import Any
from cynthia.integrations.openai.clients import GptClient


class GptService:
    system_message: str = None
    prediction_value: float = 0.5

    def __init__(self, api_key: str):
        self.client = GptClient(
            api_key=api_key,
            temperature=self.prediction_value,
        )

    def get_user_request(
            self,
            messages: list[dict[str, Any]],
            functions: list[dict[str, Any]] = None
    ):
        tools = self._build_tools_parameter(functions)
        return self.client.execute_completion(
            messages=messages,
            tools=tools
        )

    def set_system_message(self, message: str):
        self.system_message = message

    def set_prediction_value(self, value: float):
        self.prediction_value = value

    def build_messages_parameter(
            self,
            user_request: str,
            history: list[dict[str, Any]] = None
    ):
        messages = []

        if self.system_message:
            messages.append({"role": "system", "content": self.system_message})

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
