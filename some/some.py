from pymongo import MongoClient

claster = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false'

client = MongoClient(claster)


