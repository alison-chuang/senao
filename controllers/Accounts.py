from flask import (request, jsonify)

import time

failed_attempts = 0
last_failed_time = None

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
        global failed_attempts
        global last_failed_time

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'success': False, 'reason': 'Username and password are required.'}), 400

        if failed_attempts >= 5:
            if last_failed_time is not None and time.time() - last_failed_time < 60:
                remaining_time = int(60 - (time.time() - last_failed_time))
                return jsonify({'success': False, 'reason': f'Too many failed attempts. Please wait {remaining_time} seconds before trying again.'}), 429
            else:
                failed_attempts = 0
                last_failed_time = None

        valid_password = self.model.verify_account(username, password)
        if valid_password:
            failed_attempts = 0
            last_failed_time = None
            return jsonify({'success': True}), 200
        else:
            failed_attempts += 1
            last_failed_time = time.time()
            return jsonify({'success': False, 'reason': 'Invalid username or password.'}), 401
