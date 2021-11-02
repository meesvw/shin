from discord.ext import commands


async def is_mees(ctx):
    return ctx.author.id == 298890523454734336


class Devs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # Misc commands
    # geef dev team role
    @commands.command()
    @commands.check(is_mees)
    async def restore(self, ctx):
        await ctx.message.delete()
        # role = ctx.guild.get_role(750673616584048741)
        role = ctx.guild.get_role(669161981554589725)
        await ctx.author.add_roles(role)

    # # Cogs commands
    # Load cog
    @commands.command()
    @commands.check(is_mees)
    async def load(self, ctx, cog):
        try:
            self.bot.load_extension(f'cogs.{cog}')
            await ctx.send(f'`{cog} loaded`')
        except Exception as e:
            await ctx.send(f'`error: {e}`')

    # Unload cog
    @commands.command()
    @commands.check(is_mees)
    async def unload(self, ctx, cog):
        if cog == 'devs':
            return await ctx.send('`devs cannot be unloaded only updated!`')

        try:
            self.bot.unload_extension(f'cogs.{cog}')
            await ctx.send(f'`{cog} unloaded`')
        except Exception as e:
            await ctx.send(f'`error: {e}`')

    # Update cog
    @commands.command()
    @commands.check(is_mees)
    async def update(self, ctx, cog):
        try:
            self.bot.unload_extension(f'cogs.{cog}')
            self.bot.load_extension(f'cogs.{cog}')
            await ctx.send(f'`{cog} updated`')
        except Exception as e:
            await ctx.send(f'`error: {e}`')

    # # Database commands
    # poke database
    @commands.command()
    @commands.check(is_mees)
    async def poke(self, ctx):
        db = self.bot.get_cog('Database')
        return await ctx.send(await db.poke())

    # drops all logs
    @commands.command()
    @commands.check(is_mees)
    async def drop(self, ctx):
        db = self.bot.get_cog('Database')
        return await ctx.send(await db.drop())


def setup(bot):
    bot.add_cog(Devs(bot))
