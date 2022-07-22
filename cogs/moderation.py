import asyncio
import database
import discord
from datetime import datetime
from discord.ext import commands


def current_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


"""
Permissions volgorde @commands.has_any_role is:
Proxy, Hoofd Yuuto, Yuuto, Trial-Yuuto, Dev Team

IDs:
Proxy       = 669181460124532736
Hoofd Yuuto = 697198873495470090
Yuuto       = 669371769672564776
Trial-Yuuto = 705844874590552365
Dev Team    = 750673616584048741

Welkom role:
IDs:
Kazoku      = 668825700798693377
"""

team_roles = [669181460124532736, 697198873495470090, 669371769672564776, 705844874590552365, 750673616584048741]

# Excludes Trail-Yuuto
high_roles = [669181460124532736, 697198873495470090, 669371769672564776, 750673616584048741]


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # utility
    # clear messages command prefix
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(team_roles)
    async def clear(self, ctx, amount: int):
        if amount < 1:
            return await ctx.send(f'Hey {ctx.author.mention} ik heb een positief getal nodig!')

        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'Ik heb {amount} bericht(en) verwijderd!')

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(f'Hey {ctx.author.mention} je kan alleen nummers gebruiken!')

    # clear lobby command prefix
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(
        669181460124532736, 697198873495470090, 669371769672564776, 705844874590552365, 750673616584048741
    )
    async def lobby(self, ctx):
        if ctx.channel.id != 696859692684541983:
            return await ctx.send(f'Hey {ctx.author.mention} dit is niet de lobby!')

        embeds = self.bot.get_cog('Embeds')

        await ctx.channel.purge(limit=100)
        message = await ctx.channel.send('**Waarom zie ik zo weinig kanalen ?**\n'
                               'Dat komt omdat je momenteel niet geverifieerd bent. '
                               'Toegang tot de rest van de server / kanalen wordt verleend na ontvangst van de '
                               'geverifieerde rol, die handmatig wordt toegewezen door een moderator bij voltooien '
                               'van het verificatieproces.\n\n'
                               '**Waarom ben ik niet toegelaten?**\n'
                               'Dat zou kunnen omdat je niet je rollen hebt geselecteerd of je hebt niet gezegd waarom'
                               ' je de server bent gejoined.\n\n'
                               '**Hoe kan ik geverifieerd worden?**\n'
                               'Wanneer je de server joined dan moet je even je rollen selecteren en aan een moderator '
                               'vertellen waarom je de server bent gejoined! Als een moderator vindt dat jij niet past '
                               'bij onze server dan heeft de moderator het recht om jou te weigeren.')
        await message.pin()
        await self.bot.get_channel(734365925620580402).send(embed=await embeds.lobby_cleared(ctx.author))

    # show avatar command prefix
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(
        669181460124532736, 697198873495470090, 669371769672564776, 705844874590552365, 750673616584048741
    )
    async def avatar(self, ctx, user: discord.User):
        embeds = self.bot.get_cog('Embeds')
        return await ctx.send(embed=await embeds.user_avatar(user))

    # # welcome commands
    # welcome command prefix
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(
        669181460124532736, 697198873495470090, 669371769672564776, 705844874590552365, 750673616584048741
    )
    async def welkom(self, ctx, user: discord.Member):
        await ctx.message.delete()

        add_role = ctx.guild.get_role(668825700798693377)
        remove_role = ctx.guild.get_role(685607372428804104)

        if add_role in user.roles:
            return await ctx.send(f'Hey {ctx.author.mention} deze gebruiker is al toegelaten!')

        await user.remove_roles(
            remove_role,
            reason='Toegelaten tot de server'
        )

        await user.add_roles(
            add_role,
            reason='Toegelaten tot de server'
        )

        introductie_channel = self.bot.get_channel(670218992211853344)

        embeds = self.bot.get_cog('Embeds')

        await user.send(embed=await embeds.welcome_dm(user, ctx.author, introductie_channel))

        welcome_role = ctx.guild.get_role(701713402745323542)
        general_channel = self.bot.get_channel(671066993792647191)

        await self.bot.get_channel(734365925620580402).send(embed=await embeds.toegang_gegeven(ctx.author, user))
        try:
            await general_channel.send(f'{welcome_role.mention} Hiep hiep hoera, er is een nieuw lid bij genaamd '
                                       f'{user.mention} 🎉')
        except Exception as e:
            print(e)

    # weiger command prefix
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(
        669181460124532736, 697198873495470090, 669371769672564776, 705844874590552365, 750673616584048741
    )
    async def weiger(self, ctx, user: discord.Member):
        await ctx.message.delete()

        role = ctx.guild.get_role(668825700798693377)

        if ctx.author == user:
            return await ctx.send(f'Hey {ctx.author.mention} je kan jezelf niet weigeren')

        if role not in user.roles and not user.bot:
            await user.send(f'**Je bent uit Cosplayers From NL gezet {user.mention}.**\n'
                            f'Dit kwam doordat je niet geverifieerd was of ongeschikt was voor de server. '
                            f'Denk je dat dit een fout was of wil je het opnieuw proberen kan je via deze link joinen: '
                            f'\nhttps://discord.gg/AjHwdycCkh')
            await user.kick(reason='Geweigerd voor de server')
        else:
            return await ctx.send(f'Hey {ctx.author.mention} ik kan deze gebruiker niet weigeren')

        embeds = self.bot.get_cog('Embeds')
        await self.bot.get_channel(734365925620580402).send(embed=await embeds.toegang_geweigerd(ctx.author, user))

    # introductie command
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(
        669181460124532736, 697198873495470090, 669371769672564776, 705844874590552365, 750673616584048741
    )
    async def introduceer(self, ctx, user: discord.User):
        await ctx.message.delete()
        # introductie_channel = self.bot.get_channel(670218992211853344)

        embeds = self.bot.get_cog('Embeds')

        # await user.send(embed=await embeds.welcome_dm(user, ctx.author, introductie_channel))

        welcome_role = ctx.guild.get_role(701713402745323542)
        general_channel = self.bot.get_channel(671066993792647191)

        # await self.bot.get_channel(734365925620580402).send(embed=await embeds.toegang_gegeven(ctx.author, user))
        try:
            await general_channel.send(f'{welcome_role.mention} Hiep hiep hoera, er is een nieuw lid bij genaamd '
                                       f'{user.mention} 🎉')
        except Exception as e:
            print(e)

    # # warning commands
    # warn command
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(
        669181460124532736, 697198873495470090, 669371769672564776, 705844874590552365, 750673616584048741
    )
    async def warn(self, ctx, users: commands.Greedy[discord.User], *, warning='Geen redenen gegeven'):
        await ctx.message.delete()
        embeds = self.bot.get_cog("Embeds")
        for user in users:
            cosplayer = database.Cosplayer(user.id)
            if await cosplayer.add_warning(f'{ctx.author.name}#{ctx.author.discriminator}', warning):
                channel = self.bot.get_channel(719263750426984538)
                await ctx.send(embed=await embeds.warning_short(user, ctx.author))
                await channel.send(embed=await embeds.warning(user, warning, ctx.author))
            else:
                await ctx.send(embed=await embeds.error())
                break

    # show warnings command
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(
        669181460124532736, 697198873495470090, 669371769672564776, 705844874590552365, 750673616584048741
    )
    async def warnings(self, ctx, user: discord.User = None):
        await ctx.message.delete()
        embeds = self.bot.get_cog('Embeds')

        if not user:
            return await ctx.send(embed=await embeds.explain('warnings', '`warnings @hope`'))

        cosplayer = database.Cosplayer(user.id)
        user_warnings = await cosplayer.get_warnings()

        if user_warnings:
            message = await ctx.send(embed=await embeds.loading())

            emoji_list = ('◀', '❌', '▶')
            menu_number = 0

            for emoji in emoji_list:
                await message.add_reaction(emoji=emoji)

            def check(reaction, main_user):
                return main_user == ctx.author and str(reaction.emoji) in emoji_list and reaction.message.id == \
                       message.id

            await message.edit(embed=await embeds.warnings(user, user_warnings, menu_number))

            while True:
                try:
                    reaction, main_user = await self.bot.wait_for('reaction_add', timeout=20, check=check)
                    await message.remove_reaction(str(reaction.emoji), ctx.author)

                    if str(reaction.emoji) == '◀' and menu_number > 0:
                        menu_number -= 1
                    if str(reaction.emoji) == '▶' and menu_number != len(user_warnings)-1:
                        menu_number += 1
                    if str(reaction.emoji) == '❌':
                        await cosplayer.remove_warning(user_warnings[menu_number][0])
                        user_warnings = await cosplayer.get_warnings()
                        menu_number = 0

                    if user_warnings:
                        await message.edit(embed=await embeds.warnings(user, user_warnings, menu_number))
                    else:
                        await message.edit(embed=await embeds.nowarning(user))
                        await asyncio.sleep(10)
                        break
                except asyncio.TimeoutError:
                    break

            await message.delete()

        else:
            message = await ctx.send(embed=await embeds.nowarning(user))
            await asyncio.sleep(10)
            await message.delete()

    # pardon command
    @commands.command(aliases=['vergeef'])
    @commands.guild_only()
    @commands.has_any_role(
        669181460124532736, 697198873495470090, 669371769672564776, 705844874590552365, 750673616584048741
    )
    async def pardon(self, ctx, user: discord.User, warning_number=None):
        await ctx.message.delete()
        embeds = self.bot.get_cog('Embeds')

        # check if warning_number is given
        if warning_number is None:
            return await ctx.send(
                embed=await embeds.explain(
                    'pardon',
                    'Voorbeeld: `!pardon @user ID` De warning ID kan je vinden door `!warnings @user` te doen'
                )
            )

        output = await database.Cosplayer(user.id).remove_warning(warning_number)

        if output:
            channel = self.bot.get_channel(719263750426984538)
            await channel.send(embed=await embeds.pardon(user, ctx.author))
            return await ctx.send(embed=await embeds.pardon_short(user))
        elif not output:
            return await ctx.send(embed=await embeds.nopardon())
        else:
            return await ctx.send(embed=await embeds.error())

    # # mute commands
    # mute command
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(
        669181460124532736, 697198873495470090, 669371769672564776, 705844874590552365, 750673616584048741
    )
    async def mute(self, ctx, users: commands.Greedy[discord.Member]):
        embeds = self.bot.get_cog('Embeds')
        add_role = ctx.guild.get_role(671073771246845960)

        if users is None:
            return await ctx.send(embeds=await embeds.explain('!mute @gebruiker(s) redenen'))

        for user in users:
            if user.bot:
                return await ctx.send(f'{ctx.author.mention} je kan geen bots kicken')

            if user == ctx.author:
                return await ctx.send(f'{ctx.author.mention} je kan jezelf niet mute!')

            # check if user is in voice
            if user.voice:
                await user.move_to(None)

            await user.add_roles(add_role, reason=f'Muted door {ctx.author.name}')
            await ctx.send(embed=await embeds.user_muted_short(user))
            await self.bot.get_channel(734365925620580402).send(embed=await embeds.user_muted(user, ctx.author))

    # unmute command
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(
        669181460124532736, 697198873495470090, 669371769672564776, 705844874590552365, 750673616584048741
    )
    async def unmute(self, ctx, user: discord.Member):
        embeds = self.bot.get_cog('Embeds')
        remove_role = ctx.guild.get_role(671073771246845960)
        if remove_role in user.roles:
            await user.remove_roles(remove_role, reason=f'Unmuted door {ctx.author.name}')
            await ctx.send(embed=await embeds.user_unmuted_short(user))
            await self.bot.get_channel(734365925620580402).send(embed=await embeds.user_unmuted(user, ctx.author))
        else:
            await ctx.send(f'Hey {ctx.author.mention} deze persoon is al geunmute!')

    # # kick commands
    # kick command
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(
        669181460124532736, 697198873495470090, 669371769672564776, 705844874590552365, 750673616584048741
    )
    async def kick(self, ctx, users: commands.Greedy[discord.Member], *, reason=None):
        embeds = self.bot.get_cog('Embeds')
        if not users:
            return await ctx.send(embed=await embeds.explain('!kick @gebruiker(s) redenen'))

        for user in users:
            if user.bot:
                return await ctx.send(f'{ctx.author.mention} je kan geen bots kicken')

            if user == ctx.author:
                return await ctx.send(f'{ctx.author.mention} je kan jezelf niet kicken!')

            if reason is None:
                reason = 'Geen redenen opgegeven.'

            await user.kick(reason=reason)
            await self.bot.get_channel(734365925620580402).send(embed=await embeds.kick(user, ctx.author, reason))
            await ctx.send(embed=await embeds.kick_short(user))

    # # ban commands
    # ban command
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(
        669181460124532736, 697198873495470090, 669371769672564776, 750673616584048741
    )
    async def ban(self, ctx, users: commands.Greedy[discord.Member], *, reason=None):
        embeds = self.bot.get_cog('Embeds')
        log_channel = self.bot.get_channel(744259944760737795)
        community_channel = self.bot.get_channel(717814933705982083)

        if not users:
            return await ctx.send(embed=await embeds.explain('!ban @gebruiker(s) redenen'))

        for user in users:
            if user.bot:
                return await ctx.send(f'{ctx.author.mention} je kan geen bots kicken!')

            if user == ctx.author:
                return await ctx.send(f'{ctx.author.mention} je kan jezelf niet bannen!')

            if reason is None:
                reason = 'Geen redenen opgegeven.'

            await user.send(f'Je bent gebanned uit Cosplayers van NL voor deze redenen: ```text\n{reason}\n```')
            await user.ban(reason=reason)
            await log_channel.send(embed=await embeds.ban(user, ctx.author, reason))
            await ctx.send(embed=await embeds.ban_short(user))
            await community_channel.send(embed=await embeds.ban(user, ctx.author, reason))

    # # verjaardag commands
    # geef verjaardag role command
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(
        669181460124532736, 697198873495470090, 669371769672564776, 705844874590552365, 750673616584048741
    )
    async def verjaardag(self, ctx, user: discord.Member):
        if ctx.guild.get_role(670769561926369280) in user.roles:
            return await ctx.send(f'Hey {ctx.author.mention} deze persoon is al jarig!')

        await user.add_roles(ctx.guild.get_role(670769561926369280))
        await ctx.send(f'{ctx.author.mention} {user.name} is jarig!')

    # verwijder verjaardag role command
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(
        669181460124532736, 697198873495470090, 669371769672564776, 705844874590552365, 750673616584048741
    )
    async def verwijderverjaardag(self, ctx, user: discord.Member):
        if ctx.guild.get_role(670769561926369280) not in user.roles:
            return await ctx.send(f'Hey {ctx.author.mention} deze persoon is niet jarig!')

        await user.remove_roles(ctx.guild.get_role(670769561926369280))
        await ctx.send(f'{ctx.author.mention} {user.name} is niet meer jarig!')

    # Suggestie command.
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(668825700798693377)
    async def suggestie(self, ctx, *, text=None):
        await ctx.message.delete()

        if text is None:
            return await ctx.send(f'{ctx.author.mention} suggestie mag niet leeg zijn.')

        embeds = self.bot.get_cog('Embeds')
        suggestion_channel = self.bot.get_channel(722512072428224572)

        await ctx.send(f'{ctx.author.mention} je hebt een suggestie in {suggestion_channel.mention} gedaan!')

        message = await suggestion_channel.send(embed=await embeds.suggestie(ctx.author, text))

        for emoji in ('👍', '👎', '❗'):
            await message.add_reaction(emoji)

        def check(reaction, user):
            return str(reaction.emoji) == '❗' and not user.bot

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=86400, check=check)
                log_channel = self.bot.get_channel(734365925620580402)
                await log_channel.send(embed=await embeds.suggestie_report(user, message))
            except asyncio.TimeoutError:
                break


def setup(bot):
    bot.add_cog(Moderation(bot))
