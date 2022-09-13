import database
import discord
from discord.ext import commands


class Communication(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # economy
    # get user coins
    @commands.command()
    async def coins(self, ctx, user: discord.User = None):
        if not user:
            user = ctx.author

        cosplayer = database.Cosplayer(user.id)
        coins = await cosplayer.get_coins()

        if user == ctx.author:
            return await ctx.send(f'Hey {ctx.author.mention} je hebt `{coins}` coins')
        return await ctx.send(f'Hey {ctx.author.mention} {user.name} heeft `{coins}` coins')

    @commands.command()
    async def betaal(self, ctx, user: discord.User, coins: int):
        if ctx.author == user:
            return await ctx.send(f'Hey {ctx.author.mention} je kan niet jezelf betalen!')

        if coins < 1:
            return await ctx.send(f'Hey {ctx.author.mention} je moet minimaal `1` coin geven!')

        embeds = self.bot.get_cog('Embeds')

        betaler = database.Cosplayer(ctx.author.id)
        ontvanger = database.Cosplayer(user.id)

        if await betaler.get_coins() < coins:
            return await ctx.send(f'Hey {ctx.author.mention} je hebt niet genoeg coins!')

        if await ontvanger.update_coins(coins) and await betaler.update_coins(-abs(coins)):
            return await ctx.send(f'Hey {ctx.author.mention} je hebt {user.name} `{coins}` gegeven')
        else:
            return await ctx.send(embed=await embeds.error())

    # give user coins
    @commands.command()
    @commands.has_any_role(
        669181460124532736, 697198873495470090, 669371769672564776, 705844874590552365, 750673616584048741
    )
    async def doneer(self, ctx, user: discord.User, coins: int):
        cosplayer = database.Cosplayer(user.id)
        embeds = self.bot.get_cog('Embeds')
        if await cosplayer.update_coins(coins):
            if user == ctx.author:
                return await ctx.send(f'Hey {ctx.author.mention} je hebt jezelf `{coins}` gegeven!')
            return await ctx.send(f'Hey {ctx.author.mention} je hebt {user.name} `{coins}` gegeven!')
        else:
            return await ctx.send(embed=await embeds.error())

    # daily
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 79200, commands.BucketType.user)
    async def daily(self, ctx):
        cosplayer = database.Cosplayer(ctx.author.id)
        embeds = self.bot.get_cog('Embeds')
        if await cosplayer.update_coins(500):
            return await ctx.send(f'Hey {ctx.author.mention} je hebt `500` coins gekregen!')
        else:
            return await ctx.send(embed=await embeds.error())
        # self.daily.reset_cooldown(ctx)


async def setup(bot):
    await bot.add_cog(Communication(bot))
