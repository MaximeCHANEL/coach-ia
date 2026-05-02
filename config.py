from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    def __init__(self):
        self.MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
        self.MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-small-latest")
        self.DB_PATH = os.getenv("DB_PATH")
        self.APP_ENV = os.getenv("APP_ENV", "dev")

    def validate(self):
        if self.MISTRAL_API_KEY is None:
            raise ValueError("MISTRAL_API_KEY is not set in the environment variables.")

load_dotenv()
settings = Settings()
settings.validate()