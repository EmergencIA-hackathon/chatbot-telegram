import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "chatbot_db"),
        user=os.getenv("DB_USER", "chatbot_user"),
        password=os.getenv("DB_PASSWORD", "securepassword"),
        cursor_factory=RealDictCursor
    )
    return connection
