from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_URL = os.getenv("DATABASE_URL")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")
EMAIL_SECRET_KEY = os.getenv("EMAIL_SECRET_KEY")
