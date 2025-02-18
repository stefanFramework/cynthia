from typing import Any
from openai import OpenAI


class GptClient:
    def __init__(self, api_key: str, temperature: float):
        self.client = OpenAI(api_key=api_key)
        self.temperature = temperature

    def execute_completion(
            self,
            messages: list[dict[str, Any]],
            tools: list[dict[str, Any]]
    ):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            # response_format={"type": "json_object"},
            temperature=self.temperature,
            messages=messages,
            tools=tools
        )

        return response.choices[0]
