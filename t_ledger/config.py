from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


_BASE_DIR: Path = Path(__file__).resolve().parent.parent


class TGBotConfig(BaseModel):
    token: str
    ids_allowed_users_str: str

    @property
    def ids_allowed_users(self) -> set:
        return set(map(int, self.ids_allowed_users_str.strip().split("|")))


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
