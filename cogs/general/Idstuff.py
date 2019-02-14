from discord.ext import commands
from utils import colors
from utils.Help.betterhelp import BetterHelp
import discord

class IdStuff:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="getid", aliases=["id"])
    async def _id(self, ctx):
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id
        user_id = ctx.author.id
        embed = discord.Embed(title="Get ID", color=colors.random_color(), description=f"Server ID: `{guild_id}`\n"f"Channel ID: `{channel_id}`\n"f"Your ID: `{user_id}`")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(IdStuff(bot))
