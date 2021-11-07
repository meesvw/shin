import discord
from discord.ext import commands


class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # utility embeds
    # returns user avatar
    async def user_avatar(self, user):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{user.name}\'s avatar'
        )
        embed.set_image(
            url=user.avatar_url
        )
        return embed

    # returns status changed embed
    async def status_changed(self, user, status):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{user.name} heeft status veranderd',
            icon_url=user.avatar_url
        )
        embed.add_field(
            name='Nieuwe status',
            value=status
        )
        return embed

    # returns short status changed embed
    async def status_changed_short(self):
        embed = discord.Embed(
            color=discord.Colour.green()
        )
        embed.set_author(
            name='Mijn status is veranderd!'
        )
        return embed

    # returns loading embed
    async def loading(self):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name="Bereid wat dingen voor!",
            icon_url=self.bot.user.avatar_url
        )
        return embed

    # returns error embed
    async def error(self):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f"oops iets ging verkeerd..",
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Weer dit bericht?",
            value="Meld het aan een moderator of aan het dev team!"
        )
        return embed

    # # join/leave embeds
    # returns join log
    async def join_log(self, joiner):
        embed = discord.Embed(
            color=discord.Colour.green()
        )
        embed.set_author(
            name="Join | " + joiner.name + "#" + joiner.discriminator,
            icon_url=joiner.avatar_url
        )
        embed.add_field(
            name="Gebruiker: " + joiner.name + "#" + joiner.discriminator,
            value=joiner.mention,
            inline=False
        )
        embed.add_field(
            name="Gebruiker-ID: ",
            value=f'`{joiner.id}`',
            inline=False
        )
        embed.add_field(
            name="Account is gemaakt op:",
            value=joiner.created_at.strftime('%d/%m/%Y %H:%M:%S'),
            inline=False
        )
        embed.add_field(
            name="Aantal leden:",
            value=joiner.guild.member_count,
            inline=False
        )
        embed.set_thumbnail(
            url=joiner.avatar_url
        )
        return embed

    # returns welcome dm
    async def welcome_dm(self, joiner, toelater, channel):
        embed = discord.Embed(
            title=f'Hey {joiner.name}',
            description=f'Welkom in Cosplayers from NL! Vergeet niet jezelf voor te stellen in {channel.mention}'
                        f'We wensen je veel plezier! :heart:',
            color=discord.Colour.blue()
        )
        embed.set_footer(
            text=f'{toelater.name} heeft je toegang gegeven',
            icon_url=toelater.avatar_url
        )
        return embed

    # return leave embed
    async def leave_log(self, leaver):
        embed = discord.Embed(
            color=discord.Colour.red()
        )
        embed.set_author(
            name="Left | " + leaver.name + "#" + leaver.discriminator,
            icon_url=leaver.avatar_url
        )
        embed.add_field(
            name="Gebruiker: " + leaver.name + "#" + leaver.discriminator,
            value=leaver.mention,
            inline=False
        )
        embed.add_field(
            name="Gebruiker-ID: ",
            value=f'`{leaver.id}`',
            inline=False
        )
        embed.add_field(
            name="Account is gemaakt op:",
            value=leaver.created_at.strftime('%d/%m/%Y %H:%M:%S'),
            inline=False
        )
        embed.add_field(
            name="Join datum::",
            value=leaver.joined_at.strftime('%d/%m/%Y %H:%M:%S'),
            inline=False
        )
        embed.add_field(
            name="Aantal leden:",
            value=leaver.guild.member_count,
            inline=False
        )
        embed.set_thumbnail(
            url=leaver.avatar_url
        )
        return embed

    # # log embeds
    # returns lobby cleared
    async def lobby_cleared(self, clearer):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{clearer.name} heeft de lobby leeg gemaakt',
            icon_url=clearer.avatar_url
        )
        return embed

    # returns user toegelaten embed
    async def toegang_gegeven(self, toelater, toegelaten):
        embed = discord.Embed(
            color=discord.Colour.blue(),
        )
        embed.set_author(
            name=f'{toelater.name} heeft toegang gegeven aan {toegelaten.name}',
            icon_url=toelater.avatar_url
        )
        return embed

    # returns users geweigerd embed
    async def toegang_geweigerd(self, weigeraar, geweigerde):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{weigeraar.name} heeft {geweigerde.name} geweigerd',
            icon_url=weigeraar.avatar_url
        )
        return embed

    # # mute embeds
    # returns user muted embed
    async def user_muted(self, muted, muter):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{muter.name} heeft {muted.name} gemute',
            icon_url=muter.avatar_url
        )
        return embed

    # returns short user muted embed
    async def user_muted_short(self, muted):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{muted.name} is gemute',
            icon_url=muted.avatar_url
        )
        return embed

    # returns user unmuted embed
    async def user_unmuted(self, muted, unmuter):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{unmuter.name} heeft {muted.name} geunmute',
            icon_url=unmuter.avatar_url
        )
        return embed

    # returns user short unmuted embed
    async def user_unmuted_short(self, muted):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{muted.name} is geunmute',
            icon_url=muted.avatar_url
        )
        return embed

    # # warning embeds
    # returns give warning embed
    async def warning(self, user, warning, warner):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f"{user.name} is gewaarschuwd",
            icon_url=user.avatar_url
        )
        embed.add_field(
            name="Redenen",
            value=warning,
            inline=False
        )
        embed.add_field(
            name="Gegeven door",
            value=f"`{warner.name}#{warner.discriminator}`",
        )
        return embed

    # returns short give warning embed
    async def warning_short(self, user, warner):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{warner.name} heeft {user.name} gewaarschuwd',
            icon_url=warner.avatar_url
        )
        return embed

    # returns warnings not found embed
    async def nowarning(self, user):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f"{user.name} heeft geen waarschuwingen",
            icon_url=user.avatar_url
        )
        return embed

    # returns pardon warning embed
    async def pardon(self, user, vergever):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{vergever.name} heeft {user.name} vergeven'
        )
        return embed

    # returns short pardon warning embed
    async def pardon_short(self, user):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f"{user.name} is vergeven",
            icon_url=user.avatar_url
        )
        return embed

    # returns pardon not found embed
    async def nopardon(self):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name="Waarschuwing niet gevonden",
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name="Nummer correct?",
            value="Zoek de warning met `warnings @hope`"
        )
        return embed

    # # kick embeds
    # returns kick embed
    async def kick(self, user, kicker, reason):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{user.name} is gekicked',
            icon_url=user.avatar_url
        )
        embed.add_field(
            name='Redenen',
            value=reason
        )
        embed.add_field(
            name='Was lid sinds',
            value=user.joined_at.strftime("%d %b %Y"),
            inline=False
        )
        embed.set_footer(
            text=f'Kicked door {kicker.name}{kicker.discriminator}',
            icon_url=kicker.avatar_url
        )
        return embed

    # return short kick embed
    async def kick_short(self, user):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{user.name} is gekicked',
            icon_url=user.avatar_url
        )
        return embed

    # # ban embeds
    # returns ban embed
    async def ban(self, user, banner, reason):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{user.name} is verbannen',
            icon_url=user.avatar_url
        )
        embed.add_field(
            name='Redenen',
            value=reason
        )
        embed.add_field(
            name='Was lid sinds',
            value=user.joined_at.strftime("%d %b %Y"),
            inline=False
        )
        embed.set_footer(
            text=f'Verbannen door {banner.name}{banner.discriminator}',
            icon_url=banner.avatar_url
        )
        return embed

    # return short ban embed
    async def ban_short(self, user):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name=f'{user.name} is verbannen',
            icon_url=user.avatar_url
        )
        return embed

    # # uitleg commands
    # algemene help command
    async def help(self):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name='Hier zijn alle commands!',
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name='Fun',
            value='- !hug @gebruiker\n'
                  '- !pat @gebruiker\n'
                  '- !wink @gebruiker\n',
            inline=False
        )
        embed.add_field(
            name='Moderatie (Alleen voor moderators)',
            value='- !ban @gebruiker(s) redenen\n'
                  '- !kick @gebruiker(s) redenen\n'
                  '- !warn @gebruiker(s) redenen\n'
                  '- !pardon @gebruiker(s) redenen\n'
                  '- !warnings @gebruiker\n'
                  '- !mute @gebruiker\n'
                  '- !unmute @gebruiker\n'
                  '- !lobby\n'
                  '- !welkom @gebruiker\n'
                  '- !weiger @gebruiker\n'
                  '- !avatar @gebruiker',
            inline=False
        )
        embed.add_field(
            name='Bot aanpassen (Alleen voor moderators)',
            value='- !status [een status]',
            inline=False
        )
        return embed

    # command uitleg
    async def explain(self, command, uitleg):
        embed = discord.Embed(
            color=discord.Colour.blue()
        )
        embed.set_author(
            name="Command mist iets",
            icon_url=self.bot.user.avatar_url
        )
        embed.add_field(
            name=f"Hoe werkt `{command}`",
            value=uitleg
        )
        return embed


def setup(bot):
    bot.add_cog(Embeds(bot))
