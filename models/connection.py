import os

from dotenv import load_dotenv
from peewee import *

load_dotenv()

database_host = os.environ.get('DB_HOST')
database_port = os.environ.get('DB_PORT')
database_name = os.environ.get('DB_NAME')
database_user = os.environ.get('DB_USER')
database_password = os.environ.get('DB_PASSWORD')

DATABASE = MySQLDatabase(
    database_name,
    host=database_host,
    port=int(database_port),
    user=database_user,
    password=database_password
)
