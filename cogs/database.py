import os
import pymongo
import sys
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
client = pymongo.MongoClient(os.getenv("mongourl"))


def current_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # returns databases
    async def poke(self):
        return client.list_database_names()

    # drops databases
    async def drop(self):
        db = client["logs"]
        for cl in db.list_collections():
            db.drop_collection(cl["name"])
        return True

    # set user warning
    async def warn(self, user, warning, warner):
        if warning is None:
            warning = 'Geen redenen gegeven'

        try:
            db = client["logs"]
            cl = db["warnings"]
            try:
                user_warnings = cl.find_one({"_id": user.id})["warnings"]
                user_warnings[str(int(max(cl.find_one({"_id": user.id})["warnings"]))+1)] = {
                    "warning": warning,
                    "warner": f"{warner.name}#{warner.discriminator}",
                    "time": current_time()
                }
            except TypeError:
                user_warnings = {"1": {"warning": warning,
                                       "warner": f"{warner.name}#{warner.discriminator}",
                                       "time": current_time()}
                                 }
            except ValueError:
                user_warnings = {"1": {"warning": warning,
                                       "warner": f"{warner.name}#{warner.discriminator}",
                                       "time": current_time()}
                                 }
            cl.update_one(
                {"_id": user.id},
                {"$set": {"warnings": user_warnings}},
                upsert=True
            )
            return True
        except Exception:
            print(f"{current_time()} - database.py, warn function, error: {sys.exc_info()}")
        return "error"

    # returns warnings
    async def warnings(self, user):
        db = client["logs"]
        cl = db["warnings"]
        return cl.find_one({"_id": user.id})

    # remove user warning
    async def pardon(self, user, warning):
        try:
            db = client["logs"]
            cl = db["warnings"]
            try:
                user_warnings = cl.find_one({"_id": user.id})["warnings"]
                user_warnings.pop(warning)
                cl.update_one(
                    {"_id": user.id},
                    {"$set": {"warnings": user_warnings}},
                    upsert=True
                )
                return True
            except KeyError:
                return False
            except TypeError:
                return False
        except Exception:
            print(f"{current_time()} - database.py, pardon function, error: {sys.exc_info()}")
        return "error"


def setup(bot):
    bot.add_cog(Database(bot))
