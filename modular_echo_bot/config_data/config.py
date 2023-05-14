from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту

@dataclass
class Config:
    tg_bot: TgBot

def load_config(path: str | None = None) -> Config:
    env = Env()         # Создаём виртуальное окружение
    env.read_env(path)  # Бросаем в окружение путь к файлу с секретными данными
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))