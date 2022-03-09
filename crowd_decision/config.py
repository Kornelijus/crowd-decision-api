from functools import lru_cache
from pydantic import BaseSettings

@lru_cache
def get_settings():
    return Settings()

class Settings(BaseSettings):
    db_hostname: str = 'localhost:5432'
    db_user: str = 'postgres'
    db_password: str = 'postgres'
    db_name: str = 'postgres'

    app_debug: bool = True
    app_database_url: str = f'postgresql+psycopg2://{db_user}:{db_password}@{db_hostname}/{db_name}'
