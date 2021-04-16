import discord
from discord.ext import commands


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def status(self, ctx, option, *, status):
        embeds = self.bot.get_cog('Embeds')
        if option == 'watching':
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=str(status)
                )
            )
        channel = self.bot.get_channel(712680245114961943)
        await channel.send(embed=await embeds.status_changed(ctx.author, status))
        return await ctx.send(embed=await embeds.status_changed_short())


def setup(bot):
    bot.add_cog(Setup(bot))
