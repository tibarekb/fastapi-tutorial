from pydantic import BaseSettings

class Settings(BaseSettings):
    database_password: str = "localhost"
    database_username: str = "postgres"
    secret_key:str = "234hgiuhrhuhufn"
    
settings = Settings()

settings = Settings()

print(settings.database_username)