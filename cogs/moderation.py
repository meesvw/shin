import asyncio
import discord
from datetime import datetime
from discord.ext import commands


def current_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # warn command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, users: commands.Greedy[discord.User], *, warning=None):
        await ctx.message.delete()
        embeds = self.bot.get_cog("Embeds")
        db = self.bot.get_cog("Database")
        for user in users:
            output = await db.warn(user, warning, ctx.author)
            if output == "error":
                await ctx.send(embed=await embeds.error())
                break
            await ctx.send(embed=await embeds.warning(user, warning, ctx.author))
            print(f"{current_time()} - warn added to: {user.id} warning: {warning}")

    # show warnings command
    @commands.command()
    @commands.has_permissions()
    async def warnings(self, ctx, user: discord.User = None):
        await ctx.message.delete()
        embeds = self.bot.get_cog("Embeds")
        db = self.bot.get_cog("Database")
        if user:
            user_warnings = await db.warnings(user)
        else:
            return await ctx.send(embed=await embeds.explain(
                "warnings",
                "Het warnings command heeft een gebruiker nodig, voorbeeld: `warnings @mvw`"
            ))
        try:
            if user_warnings["warnings"]:
                message = await ctx.send(embed=await embeds.loading())

                dict_list = []
                for warning in user_warnings["warnings"]:
                    if warning == "_id":
                        pass
                    else:
                        dict_list.append(warning)

                emoji_list = ["◀", "▶"]
                menu_number = 0
                for emoji in emoji_list:
                    await message.add_reaction(emoji=emoji)
                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in emoji_list
                def create_embed(number):
                    embed = discord.Embed(
                        colour=discord.Colour.blue()
                    )
                    embed.set_author(
                        name=f"{user.name}'s waarschuwingen",
                        icon_url=user.avatar_url
                    )
                    embed.add_field(
                        name="Nummer",
                        value=number,
                        inline=False
                    )
                    embed.add_field(
                        name="Redenen",
                        value=user_warnings["warnings"][number]["warning"]
                    )
                    embed.add_field(
                        name="Gegeven door",
                        value=f"`{user_warnings['warnings'][number]['warner']}`"
                    )
                    embed.set_footer(
                        text=user_warnings["warnings"][number]["time"]
                    )
                    return embed

                await message.edit(embed=create_embed(dict_list[menu_number]))

                while True:
                    try:
                        reaction, user = await self.bot.wait_for("reaction_add", timeout=15, check=check)
                        await message.remove_reaction(str(reaction.emoji), ctx.author)

                        if str(reaction.emoji) == "◀" and menu_number > 0:
                            menu_number -= 1
                        if str(reaction.emoji) == "▶" and menu_number != len(dict_list)-1:
                            menu_number += 1
                        await message.edit(embed=create_embed(dict_list[menu_number]))
                    except asyncio.TimeoutError:
                        await message.delete()
                        break
            else:
                return await ctx.send(embed=await embeds.nowarning(user))
        except TypeError:
            return await ctx.send(embed=await embeds.nowarning(user))

    # pardon command
    @commands.command()
    @commands.has_permissions()
    async def pardon(self, ctx, user: discord.User, warning):
        await ctx.message.delete()
        embeds = self.bot.get_cog("Embeds")
        db = self.bot.get_cog("Database")
        output = await db.pardon(ctx.author, warning)
        if output:
            return await ctx.send(embed=await embeds.pardon(user))
        elif not output:
            return await ctx.send(embed=await embeds.nopardon())
        else:
            return await ctx.send(embed=await embeds.error())

    @commands.command()
    async def drop(self, ctx):
        db = self.bot.get_cog("Database")
        print(await db.drop())


def setup(bot):
    bot.add_cog(Moderation(bot))
