from flask import (Flask, g, request, jsonify)
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

import os
import time

from routes.accounts import accounts_bp
from models.connection import DATABASE

DEBUG = os.environ.get('DEBUG')
PORT = os.environ.get('PORT')
HOST = os.environ.get('HOST')

app = Flask(__name__)

@app.before_request
def before_request():
    g.db = DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

app.register_blueprint(accounts_bp)


if __name__ == '__main__':
    app.run(debug=True, port=PORT)