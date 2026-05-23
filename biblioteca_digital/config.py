import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    DATABASE_PATH = os.path.join(os.getcwd(), os.getenv("DATABASE_PATH", "app/db/biblioteca.db"))
    PROPRIETARIO_EMAIL = os.getenv("PROPRIETARIO_EMAIL", "admin@empresa.com")
    PROPRIETARIO_PASSWORD = os.getenv("PROPRIETARIO_PASSWORD", "senha_segura")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() in ("true", "1", "t")
