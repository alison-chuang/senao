from flask import (request, jsonify)

import time
import redis
import os
from dotenv import load_dotenv
load_dotenv()

redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')
redis_password = os.environ.get('REDIS_PASSWORD')
print(redis_port)

redis_client = redis.Redis(
    host=redis_host, 
    port=int(redis_port), 
    password=redis_password
)

class Accounts():

    def __init__(self, model):
        self.model = model

    def register(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'success': False, 'reason': 'Username and password are required.'}), 400

        if len(username) < 3 or len(username) > 32:
            return jsonify({'success': False, 'reason': 'Username length must be between 3 and 32 characters.'}), 400

        if len(password) < 8 or len(password) > 32:
            return jsonify({'success': False, 'reason': 'Password length must be between 8 and 32 characters.'}), 400

        if not any(char.isupper() for char in password) or not any(char.islower() for char in password) or not any(char.isdigit() for char in password):
            return jsonify({'success': False, 'reason': 'Password must contain at least one uppercase letter, one lowercase letter, and one number.'}), 400


        try:
            self.model.create_user(
                username=username,
                password=password
            )
            return jsonify({'success': True}), 201
        except ValueError as e:
            return jsonify({'success': False, 'reason': str(e)}), 400
        except Exception as e:
            print(e)
            return jsonify({'success': False, 'reason': 'Internal Server Error'}), 500


    def verify(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'success': False, 'reason': 'Username and password are required.'}), 400

        failed_attempts = redis_client.get(f'failed_attempts:{username}')
        if failed_attempts is None:
            failed_attempts = 0
        else:
            failed_attempts = int(failed_attempts)

        if failed_attempts >= 5:
            last_failed_time = redis_client.get(f'last_failed_time:{username}')
            if last_failed_time is not None and time.time() - float(last_failed_time) < 60:
                remaining_time = int(60 - (time.time() - float(last_failed_time)))
                return jsonify({'success': False, 'reason': f'Too many failed attempts. Please wait {remaining_time} seconds before trying again.'}), 429
            else:
                redis_client.delete(f'failed_attempts:{username}')
                redis_client.delete(f'last_failed_time:{username}')
                failed_attempts = 0

        valid_password = self.model.verify_account(username, password)
        if valid_password:
            redis_client.delete(f'failed_attempts:{username}')
            redis_client.delete(f'last_failed_time:{username}')
            return jsonify({'success': True}), 200
        else:
            failed_attempts += 1
            redis_client.set(f'failed_attempts:{username}', failed_attempts, ex=3600)  
            redis_client.set(f'last_failed_time:{username}', time.time())
            return jsonify({'success': False, 'reason': 'Invalid username or password.'}), 401
