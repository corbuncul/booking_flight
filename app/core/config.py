from typing import Optional

from pydantic import EmailStr, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    """Базовые настройки."""
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class ConfigApp(ConfigBase):
    """Настройки приложения."""
    model_config = SettingsConfigDict(env_prefix='AP_')
    title: str = Field(default='Booking flight')
    description: str = Field(default='Запись на рейсы из п. Пертоминск')
    secret: SecretStr = Field(default='SECRET')


class ConfigDB(ConfigBase):
    """Настройки базы данных."""
    model_config = SettingsConfigDict(env_prefix='DB_')
    database_url: str = Field(default='sqlite+aiosqlite:///./fastapi.db')


class ConfigSuperUser(ConfigBase):
    """Настройки для суперюзера."""
    model_config = SettingsConfigDict(env_prefix='SU_')
    superuser_email: Optional[EmailStr] = Field(default=None)
    superuser_password: Optional[SecretStr] = Field(default=None)


# class ConfigGoogle(ConfigBase):
#     """Настройки сервисного аккаунта Google-APIs."""
#     model_config = SettingsConfigDict(env_prefix='GA_')
#     type: Optional[str] = Field(default=None)
#     project_id: Optional[str] = Field(default=None)
#     private_key_id: Optional[str] = Field(default=None)
#     private_key: Optional[SecretStr] = Field(default=None)
#     client_email: Optional[EmailStr] = Field(default=None)
#     client_id: Optional[str] = Field(default=None)
#     auth_uri: Optional[str] = Field(default=None)
#     token_uri: Optional[str] = Field(default=None)
#     auth_provider_x509_cert_url: Optional[str] = Field(default=None)
#     client_x509_cert_url: Optional[str] = Field(default=None)
#     email: Optional[EmailStr] = Field(default=None)


class Config(BaseSettings):
    """Все настройки приложения."""
    app: ConfigApp = Field(default_factory=ConfigApp)
    db: ConfigDB = Field(default_factory=ConfigDB)
    superuser: ConfigSuperUser = Field(default_factory=ConfigSuperUser)
    # google: ConfigGoogle = Field(default_factory=ConfigGoogle)

    @classmethod
    def load(cls) -> "Config":
        return cls()


config = Config.load()
