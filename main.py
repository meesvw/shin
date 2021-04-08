import discord
import os
import time
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

start_time = time.time()
bot_location = f"{os.path.dirname(os.path.abspath(__file__))}/"
load_dotenv()
bot = commands.AutoShardedBot(
    command_prefix=os.getenv("prefix"),
    case_insensitive=True
)


# # functions
# returns current time
def current_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# set bot status
async def set_status():
    await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="anime!"
        )
    )


# # bot events
# on_ready event
@bot.event
async def on_ready():
    await set_status()
    print(f"{current_time()} - {bot.user.name} connected to a shard")

# # startup
# print logo
print("   __                ")
print("  / /  ___  ___  ___ ")
print(" / _ \/ _ \/ _ \/ -_)")
print("/_//_/\___/ .__/\__/ ")
print("         /_/         \n")

# check .env
check = False
if not os.path.exists(f"{bot_location}.env"):
    with open(f"{bot_location}.env", "w") as file:
        file.write("token=BotToken\nprefix=v!\nmongourl=MongoDBUrl")
        print(f"{current_time()} - Created .env file")
elif os.getenv("token") != "BotToken" and os.getenv("mongourl") != "MongoDBUrl":
    check = True
if not check:
    quit(f"{current_time()} - Please configure the .env file before starting")


# load cogs
for file in os.listdir(f"{bot_location}cogs"):
    if file.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{file[:-3]}")
        except Exception:
            print(f"{current_time()} - Error loading: {file[:-3]}")

# start bot
print(f"{current_time()} - Load time: {str(time.time()-start_time)[:5]} seconds")
bot.run(os.getenv("token"))
