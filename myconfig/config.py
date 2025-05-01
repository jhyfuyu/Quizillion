import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()


TELEBOT_TOKEN = os.getenv("TELEBOT_TOKEN")
QUESTION_TOKEN = os.getenv("LIFE_API_TOKEN")

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
)
