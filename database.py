import os
import sqlite3
from random import choice
from string import ascii_letters, digits
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
database_file = os.getenv('database')


def current_time():
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


def random_id():
    return ''.join(choice(ascii_letters + digits) for i in range(6))


def create_database():
    with sqlite3.connect(database_file) as connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS warnings (
            id TEXT PRIMARY KEY,
            user_id INT,
            warning TEXT,
            warner TEXT,
            time TEXT
        );''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS economy (
            user_id INT PRIMARY KEY,
            coins INT
        );''')
        connection.commit()


class Cosplayer:
    def __init__(self, user_id):
        self.user_id = user_id

    # economy
    async def create_wallet(self):
        with sqlite3.connect(database_file) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute('''INSERT INTO economy (user_id, coins) VALUES (?, ?)''', (self.user_id, 0))
                connection.commit()
            except Exception as e:
                print(f'{current_time()} - Error: {e}')
                return 'error'
        return True

    async def get_coins(self):
        try:
            with sqlite3.connect(database_file) as connection:
                cursor = connection.cursor()
                results = False
                while not results:
                    cursor.execute('''SELECT * FROM economy WHERE user_id=?''', (self.user_id,))
                    results = cursor.fetchall()
                    if results:
                        return results[0][1]
                    else:
                        await self.create_wallet()
        except Exception as e:
            print(f'{current_time()} - Error: {e}')
            return 'error'

    async def update_coins(self, coins: int):
        try:
            with sqlite3.connect(database_file) as connection:
                old_coins = int(await self.get_coins())
                cursor = connection.cursor()
                cursor.execute('''UPDATE economy SET coins=? WHERE user_id=?''', (old_coins + coins, self.user_id))
                connection.commit()
            return True
        except Exception as e:
            print(f'{current_time()} - Error: {e}')
            return 'error'

    # warnings
    async def get_warnings(self):
        with sqlite3.connect(database_file) as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT * FROM warnings WHERE user_id=?''', (self.user_id,))
            results = cursor.fetchall()
        return results  # RETURN LIST HERE

    async def add_warning(self, warner: str, warning: str):
        try:
            with sqlite3.connect(database_file) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    '''INSERT INTO warnings (id, user_id, warning, warner, time) VALUES (?, ?, ?, ?, ?)''', (
                        random_id(), self.user_id, warning, warner, current_time()
                    )
                )
                connection.commit()
            return True
        except Exception as e:
            print(f'{current_time()} - Error: {e}')
            return 'error'

    async def remove_warning(self, warning_number):
        try:
            with sqlite3.connect(database_file) as connection:
                cursor = connection.cursor()
                cursor.execute('''DELETE FROM warnings WHERE id=?''', (warning_number,))
                connection.commit()
            return True
        except Exception as e:
            print(f'{current_time()} - Error: {e}')
            return 'error'

    async def reset_warnings(self):
        try:
            with sqlite3.connect(database_file) as connection:
                cursor = connection.cursor()
                cursor.execute('''DELETE FROM warnings WHERE user_id=?''', (self.user_id,))
                connection.commit()
            return True
        except Exception as e:
            print(f'{current_time()} - Error: {e}')
            return 'error'


create_database()
