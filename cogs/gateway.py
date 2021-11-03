from discord.ext import commands


class Gateway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


@commands.Cog.listener()
async def on_member_join(self, member):
    if not member.bot:
        embeds = self.bot.get_cog('Embeds')
        await member.guild.get_channel(696859692684541983).send(
            f'Welkom {member.mention} in de lobby van cosfnl. '
            f'Staff komt je zo helpen!'
        )
        await member.add_roles(
            member.guild.get_role(669889906071437332),  # Hobby's banner
            member.guild.get_role(669890055472414736),  # Speciaal banner
            member.guild.get_role(685607372428804104),  # Unverified role
            reason='Nieuw lid'
        )
        await member.guild.get_channel(722771390092279819).send(embed=await embeds.join_log(member))
        await member.send(embed=await embeds.join_dm(member))


@commands.Cog.listener()
async def on_member_remove(self, member):
    if not member.bot:
        embeds = self.bot.get_cog('Embeds')
        await member.guild.get_channel(734078899297714216).send(embed=await embeds.leave_log(member))


def setup(bot):
    bot.add_cog(Gateway(bot))
