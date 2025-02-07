import psycopg
import os
from dotenv import load_dotenv
# https://docs.streamlit.io/develop/concepts/connections/secrets-management
load_dotenv()

db_name = os.getenv("DB_NAME")

DB_CONFIG = {
    "user" : os.getenv("DB_USERNAME"),
    "dbname" : db_name,
    "password" : os.getenv("DB_PASSWORD"),
    "host" : os.getenv("DB_HOST"),
    "port" : os.getenv("DB_PORT")
}


def get_connection():
    return psycopg.connect(**DB_CONFIG)


