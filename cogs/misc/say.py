from discord.ext import commands
#from utils import checks
import discord

class Say:
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_guild=True)
    @commands.command(name="say")
    async def _say(self, ctx, cid:int, *, msg:str, embed=False):
        """A simple say command!"""
        try:
            channel = self.bot.get_channel(cid)
            await channel.send(msg)
        except discord.errors.NotFound:
            user = self.bot.get_user(cid)
            await user.send(msg)

    @_say.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing an argument: `b.say <CHANNELID> <MESSAGE>`")

def setup(bot):
    bot.add_cog(Say(bot))