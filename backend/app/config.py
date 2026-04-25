from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_user: str
    mongodb_password: str
    mongodb_host: str
    mongodb_app_name: str = "trustSplitTrackerPayment"
    db_name: str = "trust_split"
    frontend_url: str = "http://localhost:7777"
    port: int = 7776
    jwt_secret: str
    access_token_expire_minutes: int = 1440
    refresh_token_expire_days: int = 90
    sendgrid_api_key: str = ""
    sendgrid_from_email: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
