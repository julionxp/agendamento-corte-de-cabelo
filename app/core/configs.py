from pydantic_settings import BaseSettings
from typing import ClassVar

from sqlalchemy.ext.declarative import declarative_base

import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = os.getenv('DB_URL')
    DBBaseModel: ClassVar = declarative_base()


    class Config():
        case_sensitive = True 


settings = Settings()