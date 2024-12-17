from os import environ as env

from dotenv import load_dotenv
from pydantic import Field, BaseModel

load_dotenv('.env-non-dev')

class PostgresTestConfig(BaseModel):
    host: str = Field(alias='TEST_POSTGRES_HOST')
    port: int = Field(alias='TEST_POSTGRES_PORT')
    login: str = Field(alias='TEST_POSTGRES_USER')
    password: str = Field(alias='TEST_POSTGRES_PASSWORD')
    database: str = Field(alias='TEST_POSTGRES_DB')

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.login}:{self.password}@{self.host}:{self.port}/{self.database}'
 

def get_postgres_config():
    return PostgresTestConfig(**env)
