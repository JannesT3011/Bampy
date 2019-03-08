from discord.ext import commands
from utils.colors import random_color
import discord
from utils.config import Config

config = Config()

class Prefix:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="prefix", invoke_without_command=True)
    @commands.cooldown(1, 10.0, commands.BucketType.user)
    async def _prefix(self, ctx):
        query = """SELECT * FROM general WHERE id = $1;"""
        row = await self.bot.db.fetchrow(query, ctx.guild.id)
        embed = discord.Embed(title="Prefixes", description=f"`{row['prefix']}` and `{config.prefix()}`", color=random_color())
        embed.set_author(icon_url=ctx.guild.icon_url, name=f"{ctx.guild.name}")
        await ctx.send(embed=embed)

    @_prefix.command(name="add", aliases=["create", "update"])
    @commands.cooldown(1, 8.0, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def _prefix_add(self, ctx, *, prefix:str):
        if len(prefix) > 15:
            raise commands.BadArgument
        else:
            query = """UPDATE general SET prefix = $1 WHERE id = $2;"""
            await self.bot.db.execute(query, prefix, ctx.guild.id)
            embed = discord.Embed(title=f"Yeah! You updated the server prefix", description=f"Prefix: `{prefix}`", color=random_color())
            await ctx.send(embed=embed)

    @_prefix_add.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Oops.. you need more permissions",description="You need the `manage guild` permission to execute this command",color=random_color())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="Oops... the prefix is to long", description="A prefix can only be 15 characters long", color=random_color())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Oh dude..", description="If you want to set a prefix, you need to type one..\n"f"`{config.prefix()}prefix add <PREFIX>`", color=random_color())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Prefix(bot))