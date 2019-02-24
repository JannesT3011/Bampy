from discord.ext import commands
from utils.embeds.get_started import GetStartd

class Start:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="start", aliases=["go", "get_started"])
    async def _setup(self, ctx):
        embed = GetStartd()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Start(bot))