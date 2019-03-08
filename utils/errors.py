from discord.ext import commands
import discord
from utils.colors import random_color
"""
CUSTOM ERRORS TO HANDLE THE EXCEPTION BETTER 
"""

class NameTooLongError(commands.BadArgument):
    pass

class TagNotFoundError(commands.CommandInvokeError):
    def __init__(self, name:str):
        self.name = name
    def __str__(self):
        return self.name

class NoServerTags(commands.BadArgument):
    pass

class TagExists(commands.BadArgument):
    pass

class GeneralErrors:
    """GENERAL COMMAND ERRORS"""
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            """COOLDOWN ERROR HANDLING"""
            embed = discord.Embed(title="Chill dude..", color=random_color(), description=str(error))
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(GeneralErrors(bot))