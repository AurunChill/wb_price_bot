from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

PROJECT_PATH = Path(__file__).parent
BOT_PATH = PROJECT_PATH / "bot"
DATA_PATH = BOT_PATH / "data"
ENV_PATH = PROJECT_PATH / ".env"

if not ENV_PATH.exists():
    raise FileNotFoundError(
        f"{ENV_PATH} does not exist. Create .env file with required variables."
    )


load_dotenv(dotenv_path=ENV_PATH, override=True)


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH), env_file_encoding="utf-8", extra="ignore"
    )


class BotSettings(EnvSettings):
    BOT_TOKEN: str

    @property
    def PRICE_INTERVAL(self): return 5

    @property
    def ADMINS(self): return ["aurunchill", "GalaninAleksei"]



class LoggingSettings(EnvSettings):
    LOG_LEVEL: str = "INFO"  # DEBUG/INFO/WARNING/ERROR/CRITICAL
    LOG_FILE: str = "bot/bot.log"
    LOG_ROTATION: str = "10 MB"  # Для ротации логов


class DatabaseSettings(EnvSettings):
    DB_TYPE: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        DATABASE_PATH = DATA_PATH / self.DB_NAME
        if self.DB_TYPE == "sqlite":
            return f"sqlite+aiosqlite:///{DATABASE_PATH}"
        raise ValueError("Unsupported database type")


class Settings:
    bot: BotSettings = BotSettings()
    database: DatabaseSettings = DatabaseSettings()
    logging: LoggingSettings = LoggingSettings()


settings = Settings()
