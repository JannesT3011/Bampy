from discord.ext import commands
import discord
from utils.colors import random_color
from utils.config import Config
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

#class NotInGuild(commands.CheckFailure):
#    pass

class GeneralErrors:
    """GENERAL COMMAND ERRORS"""
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            """COOLDOWN ERROR HANDLING"""
            embed = discord.Embed(title="Chill dude..", color=random_color(), description=str(error))
            await ctx.send(embed=embed)
        elif isinstance(ctx.channel, discord.abc.PrivateChannel):
            return await ctx.send(f"Hehe.. you cant trigger a command here! Go on a server (`Only {Config().prefix()}stats and {Config().prefix()}start`)")

def setup(bot):
    bot.add_cog(GeneralErrors(bot))