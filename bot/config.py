import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TG_TOKEN")
if not TOKEN:
    raise ValueError("Токен бота не найден. Убедитесь, что он указан в файле .env")

CONFIG = {
    "WEB_SERVER_HOST": "0.0.0.0",
    "WEB_SERVER_PORT": 443,
    "WEBHOOK_PATH": "/webhook/",
    "WEBHOOK_SSL_CERT": "webhook_cert.pem",
    "WEBHOOK_SSL_PRIV": "webhook_pkey.pem",
    "BASE_WEBHOOK_URL": "https://8.208.16.158"
}
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", os.urandom(16).hex())
