from discord.ext import commands


async def is_mees(ctx):
    return ctx.author.id == 298890523454734336


class Devs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Drops all logs
    @commands.command()
    @commands.check(is_mees)
    async def drop(self, ctx):
        db = self.bot.get_cog("Database")
        return await ctx.send(await db.drop())


def setup(bot):
    bot.add_cog(Devs(bot))
