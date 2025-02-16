import requests
from typing import Any
from abc import ABC
from openai import OpenAI


class Transformer(ABC):
    def get_user_request(
            self,
            user_request: str,
            history: list[dict[str, Any]] = None
    ):
        pass


class LLamaTransformer(Transformer):
    OLLAMA_URL = "http://localhost:11434/api/chat"

    def get_user_request(
            self,
            user_request: str,
            history: list[dict[str, Any]] = None
    ):
        body = {
            "model": "llama3.2",
            "messages": self._build_messages_parameter(user_request, history),
            "stream": False,
            "options": self._parametrize_model(),
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "run_diagnostics",
                        "description": "Returns a JSON object with diagnostics information about the client's internet service",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                }
            ],
            "tool_choice": "auto"  # Llama will decide if this function is called
        }

        return self._execute_request(request=body)

    def _build_messages_parameter(self, user_request: str, history: list[dict[str, Any]] = None):
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
            "content": user_request
        }

        messages.append(user_message)

        return messages

    def _parametrize_model(self):
        '''
            0.0 - 0.4 : Deterministic. Ideal for coding and similar activities
            0.5 - 0.8 : Medium Ideal for chat and content generation
            1.0 - 2.0 : Unpredictable. Ideal for full creativity
        '''
        return {
            "temperature": 2
        }

    def _execute_request(self, request: dict[str, Any]):
        response = requests.post(
            url=self.OLLAMA_URL,
            headers={
                "Content-Type": "application/json"
            },
            json=request,
            stream=False
        )

        if response.status_code != 200:
            raise Exception("Failed to execute")

        return response.json()



def create_text(premise):
    body = {
        "model": "llama3.2",
        "messages": [
            {
                "role": "system",
                "content": "You are a professional writer, a novelist." +
                           " Your mission is to create short stories based on a premise. " +
                           "Each story must not exceed 500 words"
            },
            {
                "role": "user",
                "content": premise
            }
        ],
        "stream": True,
        "options": {
            "temperature": 2
        }
    }

    response = requests.post(
        url="http://localhost:11434/api/chat",
        headers={
            "Content-Type": "application/json"
        },
        json=body,
        stream=True
    )

    if response.status_code != 200:
        return response.text

    return response.iter_lines(decode_unicode=True)
