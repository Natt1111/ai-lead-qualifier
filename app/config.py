import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
        self.AIRTABLE_TOKEN: str = os.getenv("AIRTABLE_TOKEN", "")
        self.AIRTABLE_BASE_ID: str = os.getenv("AIRTABLE_BASE_ID", "")
        self.AIRTABLE_TABLE_NAME: str = os.getenv("AIRTABLE_TABLE_NAME", "Leads")

    def validate(self) -> None:
        missing = [
            k for k in ("ANTHROPIC_API_KEY", "AIRTABLE_TOKEN", "AIRTABLE_BASE_ID")
            if not getattr(self, k)
        ]
        if missing:
            raise EnvironmentError(f"Missing required env vars: {', '.join(missing)}")


settings = Settings()
