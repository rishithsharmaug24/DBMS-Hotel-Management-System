from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "1q!2w@3e#4r$5t%"  # your actual password
    DB_NAME: str = "hotel_management_system"
    
    # API settings
    API_TITLE: str = "Hotel Management System API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # SQL files directory
    SQL_FILES_DIR: str = "./database"
    
    class Config:
        env_file = ".env"
    
    @property
    def DATABASE_URL(self) -> str:
        # Encode the password to handle special characters
        encoded_password = quote_plus(self.DB_PASSWORD)
        return f"mysql+pymysql://{self.DB_USER}:{encoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

# Instantiate settings
settings = Settings()

# Example usage
print(settings.DATABASE_URL)
