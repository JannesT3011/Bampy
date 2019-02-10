from discord.ext import commands
from utils import config

class Readme:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="readme", aliases=["info"])
    async def _readme(self, ctx):
        with open("./README.md", encoding="utf-8") as fp:
            readme = fp.read()
        await ctx.send(f"```html\n {readme} ```")

def setup(bot):
    bot.add_cog(Readme(bot))