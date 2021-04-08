from discord.ext import commands


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def status(self, ctx):
        return


def setup(bot):
    bot.add_cog(Setup(bot))
