from langchain_mistralai import ChatMistralAI
from config import settings

def get_llm(temperature: float = 0.3):
    return ChatMistralAI(
        model=settings.MISTRAL_MODEL,
        temperature=temperature,
        timeout=30
    )