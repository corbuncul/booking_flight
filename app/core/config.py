from typing import Optional

from pydantic import EmailStr, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    """Базовые настройки."""

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )


class ConfigApp(ConfigBase):
    """Настройки приложения."""

    model_config = SettingsConfigDict(env_prefix='AP_')
    title: str = Field(default='Booking flight')
    description: str = Field(default='Запись на рейсы из п. Пертоминск')
    secret_key: SecretStr = Field(default='SECRET')
    host: str = Field(default='localhost')


class ConfigDB(ConfigBase):
    """Настройки базы данных."""

    model_config = SettingsConfigDict(env_prefix='DB_')
    database_url: str = Field(default='sqlite+aiosqlite:///./fastapi.db')
    name: str = Field(default='flight')
    user: str = Field(default='pg_user')
    password: SecretStr = Field(default='pg_password')
    host: str = Field(default='localhost')
    port: int = Field(default=5432)


class ConfigRedis(ConfigBase):
    """Настройки Redis."""

    model_config = SettingsConfigDict(env_prefix='REDIS_')
    host: str = Field(default='redis')
    port: int = Field(default=6379)
    db: int = Field(default=0)


class ConfigBot(ConfigBase):
    """Настройка бота."""

    model_config = SettingsConfigDict(env_prefix='BOT_')
    token: SecretStr = Field(default=None)
    username: str = Field(default='BOT')
    name: str = Field(default='BOT')


class ConfigSuperUser(ConfigBase):
    """Настройки для суперюзера."""

    model_config = SettingsConfigDict(env_prefix='ADMIN_')
    email: Optional[EmailStr] = Field(default=None)
    password: Optional[SecretStr] = Field(default=None)
    username: Optional[str] = Field(default='admin')
    name: Optional[str] = Field(default='John')
    surname: Optional[str] = Field(default='Doe')
    tg_id: Optional[int] = Field(default=123456789)
    tg_username: Optional[str] = Field(default='@admin')
    birthday: Optional[str] = Field(default='2000-01-01')
    phone: Optional[str] = Field(default='+79991234567')


class Config(BaseSettings):
    """Все настройки приложения."""

    app: ConfigApp = Field(default_factory=ConfigApp)
    redis: ConfigRedis = Field(default_factory=ConfigRedis)
    bot: ConfigBot = Field(default_factory=ConfigBot)
    db: ConfigDB = Field(default_factory=ConfigDB)
    superuser: ConfigSuperUser = Field(default_factory=ConfigSuperUser)

    @classmethod
    def load(cls) -> 'Config':
        return cls()


config = Config.load()
