import asyncio
import discord
import os
from datetime import datetime, timedelta
from discord.ext import commands
from dotenv import load_dotenv


# mark bot as running for panel
print('started')

bot_location = f'{os.path.dirname(os.path.abspath(__file__))}/'
load_dotenv()
intents = discord.Intents.default()
intents.members = True
bot = commands.AutoShardedBot(
    command_prefix=os.getenv('prefix'),
    case_insensitive=True,
    help_command=None,
    intents=intents
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


# on_member_join event
@bot.event
async def on_member_join(member):
    embeds = bot.get_cog('Embeds')
    await member.add_roles(
        member.guild.get_role(669889906071437332),
        member.guild.get_role(669890055472414736),
        member.guild.get_role(685607372428804104),
        reason='Joined server'
    )
    regels_channel = 669161755972206629
    roles_channel = 935961075407523900
    await bot.get_channel(722771390092279819).send(embed=await embeds.join_log(member))
    await bot.get_channel(696859692684541983).send(
        f'Welkom {member.mention}! Lees alvast de <#{regels_channel}> en selecteer je <#{roles_channel}>, '
        f'een <@&669371769672564776> komt je zo snel mogelijk helpen! <:KellyHappyMood:720436790913269802>'
    )


# on_member_remove event
@bot.event
async def on_member_remove(member):
    embeds = bot.get_cog('Embeds')
    await bot.get_channel(734078899297714216).send(embed=await embeds.leave_log(member))


# on_command_error event
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        return await ctx.send(f'Hey {ctx.author.mention} je hebt niet genoeg rechten hiervoor!')

    if isinstance(error, commands.MissingPermissions):
        return await ctx.send(f'Hey {ctx.author.mention} je hebt niet genoeg rechten hiervoor!')

    if isinstance(error, commands.CommandNotFound):
        return await ctx.send(f'Hey {ctx.author.mention} ik ken dat command niet!')

    if isinstance(error, commands.UserNotFound):
        return await ctx.send(f'Hey {ctx.author.mention} ik kan die gebruiker niet vinden...')

    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send(
            f'{str(error).split(" ")[0]} moet worden ingevuld! '
            f'Voorbeeld: `!{ctx.command.name} {str(error).split(" ")[0]}`'
        )

    if isinstance(error, commands.CommandOnCooldown):
        time = str(timedelta(seconds=error.retry_after)).split(':')
        message = await ctx.send(
            f'Hey {ctx.author.mention} Je moet `{time[0]}`uur `{time[1]}`minuten en `{(time[2])[:2]}` seconden wachten!'
        )

        for i in range(1, 5):
            time = str(timedelta(seconds=error.retry_after - i)).split(':')
            await message.edit(
                content=f'Hey {ctx.author.mention} Je moet `{time[0]}`uur `{time[1]}`minuten en `{(time[2])[:2]}` seconden wachten!'
            )
            await asyncio.sleep(1)
        return await message.delete()

# check .env
check = False
if not os.path.exists(f'{bot_location}.env'):
    with open(f'{bot_location}.env', 'w') as file:
        file.write('token=BotToken\nprefix=!\ndatabase=data.db')
        print(f'{current_time()} - Created .env file')
elif os.getenv('token') == 'BotToken':
    quit(f'{current_time()} - Please configure the .env file before starting')

# load cogs
for file in os.listdir(f'{bot_location}cogs'):
    if file.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{file[:-3]}')
        except Exception as e:
            print(f'{current_time()} - Error loading: {file[:-3]} || {e}')

# print logo
print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
print(
    """
 _____ _     _       
/  ___| |   (_)      
\ `--.| |__  _ _ __  
 `--. \ '_ \| | '_ \ 
/\__/ / | | | | | | |
\____/|_| |_|_|_| |_|
    """
)

# start bot
bot.run(os.getenv('token'))
