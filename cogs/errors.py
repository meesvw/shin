from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Error handler on_command_error
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # return command unknown
        if isinstance(error, commands.CommandNotFound):
            return

        # return command missing arguments
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"`{error}`")

        # return command missing permissions
        if isinstance(error, commands.MissingPermissions):
            return


def setup(bot):
    bot.add_cog(Errors(bot))
