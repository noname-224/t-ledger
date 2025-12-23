from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


_BASE_DIR: Path = Path(__file__).resolve().parent.parent


class TGBotConfig(BaseModel):
    token: str


class TBankConfig(BaseModel):
    token: str
    base_url: str


class Settings(BaseSettings):
    tgbot: TGBotConfig
    tbank: TBankConfig

    model_config = SettingsConfigDict(
        env_file=_BASE_DIR / ".env",
        env_nested_delimiter="__",
        case_sensitive=False,
    )


settings = Settings()  # noqa
