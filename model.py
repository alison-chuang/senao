import os

from flask_bcrypt import generate_password_hash,check_password_hash
from peewee import *
from dotenv import load_dotenv
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

class Account(Model):
    username = CharField(unique=True)
    password = CharField(max_length=255)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, password):
        print(f"register: {password}")
        hash = generate_password_hash(password)
        print(hash)
        try:
            Account.create(
                username=username,
                password=hash,
               )
        except IntegrityError:
            raise ValueError("Account already exists")

    def verify_account(username, password):
        user = Account.select().where(Account.username == username).first()
        if user and check_password_hash(user.password, password):
            return True
        else:
            return False


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Account], safe=True)
    DATABASE.close()
