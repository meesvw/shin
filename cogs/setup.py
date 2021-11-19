import discord
from discord.ext import commands


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def help(self, ctx):
        embeds = self.bot.get_cog('Embeds')
        await ctx.send(f':mailbox_with_mail: {ctx.author.mention} ik heb je een DM gestuurd!')
        return await ctx.author.send(embed=await embeds.help())

    @commands.command()
    @commands.has_any_role(
        669181460124532736, 697198873495470090, 669371769672564776, 705844874590552365, 750673616584048741
    )
    async def status(self, ctx, *, status):
        embeds = self.bot.get_cog('Embeds')
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=status
            )
        )
        channel = self.bot.get_channel(712680245114961943)
        await channel.send(embed=await embeds.status_changed(ctx.author, status))
        return await ctx.send(embed=await embeds.status_changed_short())


def setup(bot):
    bot.add_cog(Setup(bot))
