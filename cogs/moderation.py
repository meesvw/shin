import asyncio
import discord
from datetime import datetime
from discord.ext import commands


def current_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # utility
    # show avatar command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def avatar(self, ctx, user: discord.User):
        embeds = self.bot.get_cog('Embeds')
        return await ctx.send(embed=await embeds.user_avatar(user))

    # # warning commands
    # warn command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def warn(self, ctx, users: commands.Greedy[discord.User], *, warning=None):
        await ctx.message.delete()
        embeds = self.bot.get_cog("Embeds")
        db = self.bot.get_cog("Database")
        for user in users:
            output = await db.warn(user, warning, ctx.author)
            if output == "error":
                await ctx.send(embed=await embeds.error())
                break
            channel = self.bot.get_channel(719263750426984538)
            await ctx.send(embed=await embeds.warning_short(user, ctx.author))
            await channel.send(embed=await embeds.warning(user, warning, ctx.author))
            print(f"{current_time()} - warn added to: {user.id} warning: {warning}")

    # show warnings command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def warnings(self, ctx, warnings_user: discord.User=None):
        await ctx.message.delete()
        embeds = self.bot.get_cog("Embeds")
        db = self.bot.get_cog("Database")
        if warnings_user:
            user_warnings = await db.warnings(warnings_user)
        else:
            return await ctx.send(embed=await embeds.explain(
                "warnings",
                f"`warnings @hope`"))
        try:
            if user_warnings["warnings"]:
                message = await ctx.send(embed=await embeds.loading())

                dict_list = []
                for warning in user_warnings["warnings"]:
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
                        name=f"{warnings_user.name}'s waarschuwing {number}",
                        icon_url=warnings_user.avatar_url
                    )
                    embed.add_field(
                        name="Redenen",
                        value=user_warnings["warnings"][number]["warning"]
                    )
                    embed.set_footer(
                        text=f'Door: {user_warnings["warnings"][number]["warner"]} - {user_warnings["warnings"][number]["time"]}'
                    )
                    return embed

                await message.edit(embed=create_embed(dict_list[menu_number]))

                while True:
                    try:
                        reaction, user = await self.bot.wait_for("reaction_add", timeout=20, check=check)
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
                return await ctx.send(embed=await embeds.nowarning(warnings_user))
        except TypeError:
            return await ctx.send(embed=await embeds.nowarning(warnings_user))

    # pardon command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def pardon(self, ctx, user: discord.User, warning=None):
        await ctx.message.delete()
        embeds = self.bot.get_cog("Embeds")
        db = self.bot.get_cog("Database")
        output = await db.pardon(ctx.author, warning)
        if warning is None:
            return await ctx.send(embed=await embeds.explain(
                "pardon",
                "|`!pardon @hope 1`| De 1 is de waarschuwing die je kan vinden door `!warnings @hope` te doen"))
        if output:
            channel = self.bot.get_channel(719263750426984538)
            await channel.send(embed=await embeds.pardon(user, ctx.author))
            return await ctx.send(embed=await embeds.pardon_short(user))
        elif not output:
            return await ctx.send(embed=await embeds.nopardon())
        else:
            return await ctx.send(embed=await embeds.error())

    # # ban commands
    # ban command
    @commands.command()
    @commands.has_any_role('Proxy', 'Hoofd Yuuto', 'Yuuto', 'Trail-Yuuto', 'Dev Team')
    async def ban(self, ctx, users: commands.Greedy[discord.User], *, reason=None):
        db = self.bot.get_cog('Database')
        embeds = self.bot.get_cog('Embeds')
        # for user in users:
        #     if reason is None:
        #         reason = 'quick ban'
        #     await ctx.guild.ban(user, reason=reason)
        return


def setup(bot):
    bot.add_cog(Moderation(bot))
