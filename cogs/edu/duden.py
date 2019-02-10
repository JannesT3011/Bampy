import duden
import discord
from discord.ext import commands
from utils import colors

class Duden:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="duden")
    async def _duden(self, ctx, word):
        """Search a word in the duden (German only!)"""
        get = duden.get(word)
        if get != None:
            embed = discord.Embed(
                title=f"DudenSearch ~ {word}",
                description=f"```{get}```",
                color=int(colors.random_color())
            )
            await ctx.send(embed=embed)
        else:
            await self.error(ctx.channel, word)

    async def error(self, channel, word):
        embed = discord.Embed(
            title=f"Cant find `{word}`!",
            description="Try another one!"
        )
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Duden(bot))