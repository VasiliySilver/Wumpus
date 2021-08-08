# from pymongo import MongoClient
from db.readconfig import read_config_params
from motor.motor_asyncio import AsyncIOMotorClient


def get_client():
    try:
        # method will read the env file and return the config object
        params = read_config_params()

        # reading the parameters from the config object
        usr = params.get('MONGO', 'username')
        pwd = params.get('MONGO', 'password')
        host = params.get('MONGO', 'host')
        port = params.get('MONGO', 'port')

        # connect to mongodb
        # connection_string = 'mongodb://mongoadmin:secret@mongo:27017/'
        connection_string = 'mongodb://' + usr + ':' + pwd + '@' + host + ':' + port + '/'
        # other_client = MongoClient(connection_string)
        client = AsyncIOMotorClient(connection_string)
        return client

    except Exception as error:
        print(error)
