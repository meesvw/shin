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
        dev_role = ctx.guild.get_role(750673616584048741)
        normal_role = ctx.guild.get_role(668825700798693377)
        remove_role = ctx.guild.get_role(685607372428804104)
        await ctx.author.remove_roles(remove_role)
        await ctx.author.add_roles(normal_role)
        await ctx.author.add_roles(dev_role)

    # # Cogs commands
    # Load cog
    @commands.command()
    @commands.check(is_mees)
    async def load(self, ctx, cog: str):
        try:
            self.bot.load_extension(f'cogs.{cog}')
            await ctx.send(f'`{cog} loaded`')
        except Exception as e:
            await ctx.send(f'`error: {e}`')

    # Unload cog
    @commands.command()
    @commands.check(is_mees)
    async def unload(self, ctx, cog: str):
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
    async def update(self, ctx, cog: str):
        try:
            self.bot.unload_extension(f'cogs.{cog}')
            self.bot.load_extension(f'cogs.{cog}')
            await ctx.send(f'`{cog} updated`')
        except Exception as e:
            await ctx.send(f'`error: {e}`')


async def setup(bot):
    await bot.add_cog(Devs(bot))
