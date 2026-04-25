from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_user: str
    mongodb_password: str
    mongodb_host: str
    mongodb_app_name: str = "trustSplitTrackerPayment"
    db_name: str = "trust_split"
    frontend_url: str = "http://localhost:7777"
    port: int = 7776

    class Config:
        env_file = ".env"

settings = Settings()
