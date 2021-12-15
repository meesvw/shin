import os
import pymongo
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
client = pymongo.MongoClient(os.getenv('mongourl'))


def current_time():
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


class Cosplayer:
    def __init__(self, user_id):
        self.user_id = user_id

    # # warning system
    async def get_warnings(self):
        return client['logs']['warnings'].find_one({'_id': self.user_id})

    async def add_warning(self, warner: str, warning: str):
        try:
            cl = client['logs']['warnings']
            try:
                user_warnings = cl.find_one(({'_id': self.user_id}))['warnings']

                # Check if lower warning number is available
                warn_number = 0
                for i in range(int(max(user_warnings))):
                    try:
                        user_warnings[str(i)]
                    except KeyError:
                        warn_number = i

                warn_number = int(max(user_warnings)) + 1 if warn_number == 0 else warn_number

                user_warnings[str(warn_number)] = {
                    'warning': warning,
                    'warner': warner,
                    'time': current_time()
                }
            except (TypeError, ValueError):
                user_warnings = {'1': {'warning': warning, 'warner': warner, 'time': current_time()}}
            cl.update_one({'_id': self.user_id}, {'$set': {'warnings': user_warnings}}, upsert=True)
            return True
        except Exception as e:
            print(f'{current_time()} - Error: {e}')
            return 'error'

    async def remove_warning(self, warning_number):
        try:
            cl = client['logs']['warnings']
            try:
                user_warnings = cl.find_one({'_id': self.user_id})['warnings']
                user_warnings.pop(warning_number)
                cl.update_one({'_id': self.user_id}, {'$set': {'warnings': user_warnings}}, upsert=True)
                return True
            except (KeyError, TypeError):
                return False
        except Exception as e:
            print(f'{current_time()} - Error: {e}')
            return 'error'

    async def reset_warnings(self):
        try:
            client['logs']['warnings'].delete_one({'_id': self.user_id})
            return True
        except Exception as e:
            print(f'{current_time()} - Error: {e}')
            return 'error'
