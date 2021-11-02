from discord.ext import commands


class Channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Voegt mensen toe aan de NSFW channel
    @commands.command()
    async def nsfw(self, ctx):
        channel = self.bot.get_channel(694616201577496626)
        permissions = channel.overwrites_for(ctx.author)
        permissions.update(read_messages=True, send_messages=True)
        await channel.set_permissions(ctx.author, overwrite=permissions, reason='NSFW toegang gekregen')
        await ctx.message.delete()
        await ctx.author.send('Je hebt toegang gekregen tot het NSFW kanaal')


def setup(bot):
    bot.add_cog(Channels(bot))
