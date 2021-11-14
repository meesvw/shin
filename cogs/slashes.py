from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class Slashes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='ping',
        guild_ids=[647884034676097056],
        description='Responds with pong!'
    )
    async def _ping(self, ctx: SlashContext):
        await ctx.send('Pong!')

    @commands.command()
    async def ping(self, ctx):
        return await ctx.send('Pong!')


def setup(bot):
    bot.add_cog(Slashes(bot))
