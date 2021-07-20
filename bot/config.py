import os
from dotenv import load_dotenv


load_dotenv()

CLUSTER = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false'

TOKEN = os.getenv('TOKEN')
