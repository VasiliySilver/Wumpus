import motor.motor_asyncio
from aiogram import Bot

from bot import config


class User:

    def __init__(self, name, tgid):
        self.tgid = tgid
        self.name = name

class UserDb:
    from pymongo import MongoClient
    # ключ для работы с базой
    cluster = config.CLUSTER
    # побключие к клиенту базы данных, может находиться на разных портах
    client = motor.motor_asyncio.AsyncIOMotorClient(cluster)
    # база данных с которой работаю
    db = client["user_db"]
    # таблица с которой работаю
    my_table = db.my_table

    def create_user(self, tg_id):
        pass







