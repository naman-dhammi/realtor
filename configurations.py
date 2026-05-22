import os

from dotenv import load_dotenv

load_dotenv(override=True)

# Mongo DB
MONGO_DB_CONNECTION: str = os.environ.get("MONGO_DB_CONNECTION")
MONGO_DB_DATABASE: str = os.environ.get("MONGO_DB_DATABASE")
MONGO_DB_REAL_ESTATE_TABLE: str = os.environ.get("MONGO_DB_REAL_ESTATE_TABLE")
MONGO_DB_USER: str = os.environ.get("MONGO_DB_USERS")

# Owner
CONTACT_NUMBER: str = os.environ.get("CONTACT_NUMBER")
