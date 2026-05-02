import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# 1. Add your project root to path so Python finds the 'src' folder
sys.path.append(os.getcwd())

# 2. Load your .env file
load_dotenv()

# 3. Import your Base and models for 'autogenerate'
from src.config.db import Base
from src.schemas.schema import User, ChatSession, Message

# 4. Set target_metadata (around line 21 in your screenshot)
target_metadata = Base.metadata

config = context.config

# 5. Silently overwrite the URL with your actual DATABASE_URL from .env
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)