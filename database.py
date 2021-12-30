import os
import pymongo
import random
import string
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
client = pymongo.MongoClient(os.getenv('mongourl'))


def current_time():
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


def random_id():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))


class Cosplayer:
    def __init__(self, user_id):
        self.user_id = user_id

    async def get_warnings(self):
        return list(client['logs']['warnings'].find({'user_id': self.user_id}))

    async def add_warning(self, warner: str, warning: str):
        try:
            cl = client['logs']['warnings']

            rid = random_id()
            while cl.find_one({'_id': rid}):
                rid = random_id()

            cl.insert_one({
                '_id': rid,
                'user_id': self.user_id,
                'warning': warning,
                'warner': warner,
                'time': current_time()
            })

            return True
        except Exception as e:
            print(f'{current_time()} - Error: {e}')
            return 'error'

    async def remove_warning(self, warning_number):
        try:
            client['logs']['warnings'].delete_one({'_id': warning_number, 'user_id': self.user_id})
            return True
        except Exception as e:
            print(f'{current_time()} - Error: {e}')
            return 'error'

    async def reset_warnings(self):
        try:
            client['logs']['warnings'].delete_many({'user_id': self.user_id})
            return True
        except Exception as e:
            print(f'{current_time()} - Error: {e}')
            return 'error'
