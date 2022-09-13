import discord
import json
import urllib.request
from discord.ext import commands


class Socializing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hug(self, ctx, user: discord.User):
        link = json.load(urllib.request.urlopen('https://some-random-api.ml/animu/hug'))['link']

        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_image(
            url=link
        )
        await ctx.send(f'{ctx.author.mention} knuffelt {user.mention}', embed=embed)

    @commands.command()
    async def pat(self, ctx, user: discord.User):
        link = json.load(urllib.request.urlopen('https://some-random-api.ml/animu/pat'))['link']

        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_image(
            url=link
        )
        await ctx.send(f'{ctx.author.mention} patted {user.mention}', embed=embed)

    @commands.command()
    async def wink(self, ctx, user: discord.User):
        link = json.load(urllib.request.urlopen('https://some-random-api.ml/animu/wink'))['link']

        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_image(
            url=link
        )
        await ctx.send(f'{ctx.author.mention} winked at {user.mention}', embed=embed)


async def setup(bot):
    await bot.add_cog(Socializing(bot))
