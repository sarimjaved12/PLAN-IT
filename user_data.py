import json
import os

users_file = 'users.json'

def load_users():
    try:
        with open(users_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_user(username, password):
    users = load_users()
    users[username] = password
    with open(users_file, 'w') as file:
        json.dump(users, file, indent=4)