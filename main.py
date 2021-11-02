import discord
import os
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

bot_location = f'{os.path.dirname(os.path.abspath(__file__))}/'
load_dotenv()
bot = commands.AutoShardedBot(
    command_prefix=os.getenv('prefix'),
    case_insensitive=True,
    help_command=None
)


# # functions
# returns current time
def current_time():
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


# set bot status
async def set_status():
    await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching,
            name='anime!'
        )
    )


# # bot events
# on_ready event
@bot.event
async def on_ready():
    print(f'{current_time()} - {bot.user.name} connected to a shard')


# on_member_join event (NOT FINISHED)
@bot.event
async def on_member_join(member):
    embeds = bot.get_cog('Embeds')
    await member.add_roles(
        member.guild.get_role(669889906071437332),
        member.guild.get_role(669890055472414736),
        member.guild.get_role(685607372428804104),
        reason='Joined server'
    )
    await bot.get_channel(722771390092279819).send(embed=await embeds.join_log(member))
    await member.send(embed=await embeds.join_dm(member))


# on_member_remove event
@bot.event
async def on_member_remove(member):
    embeds = bot.get_cog('Embeds')
    await bot.get_channel(734078899297714216).send(embed=await embeds.user_leave(member))


# on_command_error event
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send(f'Hey {ctx.author.mention} je hebt niet genoeg rechten hiervoor!')

    if isinstance(error, commands.CommandNotFound):
        return await ctx.send(f'Hey {ctx.author.mention} ik ken dat command niet!')

    if isinstance(error, commands.UserNotFound):
        return await ctx.send(f'Hey {ctx.author.mention} ik kan die gebruiker niet vinden...')

    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send(f'`{error}`')

# check .env
check = False
if not os.path.exists(f'{bot_location}.env'):
    with open(f'{bot_location}.env', 'w') as file:
        file.write('token=BotToken\nprefix=!\nmongourl=MongoDBUrl')
        print(f'{current_time()} - Created .env file')
elif os.getenv('token') != 'BotToken' and os.getenv('mongourl') != 'MongoDBUrl':
    check = True
if not check:
    quit(f'{current_time()} - Please configure the .env file before starting')


# load cogs
for file in os.listdir(f'{bot_location}cogs'):
    if file.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{file[:-3]}')
        except Exception as e:
            print(f'{current_time()} - Error loading: {file[:-3]} || {e}')

# start bot
bot.run(os.getenv('token'))
