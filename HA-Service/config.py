# config.py
import os

class BaseConfig:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', 5432)
    DB_NAME = os.getenv('DB_NAME', 'config_db')
    DB_USER = os.getenv('DB_USER', 'config_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'supersecret')

config = BaseConfig()
