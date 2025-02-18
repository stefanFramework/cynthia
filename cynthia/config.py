import os

from dotenv import load_dotenv

load_dotenv(".env")


class Config:
    OPENAI_KEY = os.getenv("OPENAI_KEY")

    CHAT_SYSTEM_MESSAGE = ("You are a Technical support assistant. "
                           "Your mission is to provide a diagnostic to a customer. "
                           "You have to be kind and make clear and short explanations")

    # 0.0 - 0.4: Deterministic.Ideal for coding and similar activities
    # 0.5 - 0.8: Medium Ideal for chat and content generation
    # 1.0 - 2.0: Unpredictable.Ideal for full creativity
    CHAT_TEMPERATURE = os.getenv("CHAT_TEMPERATURE", 0.8)


current_config = Config()
