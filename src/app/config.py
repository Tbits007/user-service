from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigModel(BaseSettings):
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


class RabbitMQConfig(ConfigModel):
    host: str = Field(alias='RABBITMQ_HOST')
    port: int = Field(alias='RABBITMQ_PORT')
    login: str = Field(alias='RABBITMQ_USER')
    password: str = Field(alias='RABBITMQ_PASS')

    
class PostgresConfig(ConfigModel):
    host: str = Field(alias='POSTGRES_HOST')
    port: int = Field(alias='POSTGRES_PORT')
    login: str = Field(alias='POSTGRES_USER')
    password: str = Field(alias='POSTGRES_PASSWORD')
    database: str = Field(alias='POSTGRES_DB')

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.login}:{self.password}@{self.host}:{self.port}/{self.database}'


class Config(ConfigModel):
    rabbitmq: RabbitMQConfig 
    postgres: PostgresConfig
