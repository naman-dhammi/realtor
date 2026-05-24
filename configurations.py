import os

from dotenv import load_dotenv

load_dotenv(override=True)

# Mongo DB
MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
MONGO_DB_CLUSTER = os.getenv("MONGO_DB_CLUSTER")
MONGO_DB_CONNECTION: str = rf"mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@dhammi-enterprise-clust.inkw6eu.mongodb.net/?appName={MONGO_DB_CLUSTER}"
MONGO_DB_DATABASE: str = os.environ.get("MONGO_DB_DATABASE")
MONGO_DB_REAL_ESTATE_TABLE: str = os.environ.get("MONGO_DB_REAL_ESTATE_TABLE")
MONGO_DB_USER: str = os.environ.get("MONGO_DB_USERS")

# Owner
CONTACT_NUMBER: str = os.environ.get("CONTACT_NUMBER")
