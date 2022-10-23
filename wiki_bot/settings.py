from pydantic import BaseSettings


class Settings(BaseSettings):
    token: str

    class Config:
        env_file = '.etl.env.sample', '.env'
        env_file_encoding = 'utf-8'
