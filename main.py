from cynthia.config import current_config
from cynthia.integrations.openai.services import GptService
from cynthia.utils import run_diagnostics, func_tools, handle_tool_call
from cynthia.ui import launch_chat_interface

gpt = GptService(current_config.OPENAI_KEY)
gpt.set_system_message(current_config.CHAT_SYSTEM_MESSAGE)
gpt.set_prediction_value(current_config.CHAT_TEMPERATURE)


def chat(text, history):

    messages = gpt.build_messages_parameter(user_request=text, history=history)

    result = gpt.get_user_request(messages, functions=func_tools())

    if result.finish_reason == "tool_calls":
        message = result.message
        function_result = handle_tool_call(message)

        show_messages = []
        show_message = message.model_dump()

        if not message.content:
            show_message["content"] = "Let me run a quick diagnostics of your internet connection. Please hold"

        show_messages.append(show_message)

        messages.append(show_message)
        messages.append(function_result)

        result = gpt.get_user_request(messages)
        show_messages.append(result.message.model_dump())
        yield show_messages
        return

    yield result.message.content


launch_chat_interface(chat_function=chat)
