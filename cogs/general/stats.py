from discord.ext import commands
from utils.colors import random_color
from disputils import BotEmbedPaginator
import discord
import psutil

class Stats:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="stats", aliases=["bampy", "info"], invoke_without_command=True)
    @commands.cooldown(2, 5.0, commands.BucketType.user)
    async def _stats(self, ctx):
        """INFORMATIONS ABOUT THE BOT"""
        embed = [discord.Embed(title=f"{self.bot.user.name} ~ Stats", color=random_color(),
                               description=f"**Servers:** `{len(self.bot.guilds)}`\n"
                                           f"**Users:** `{len(self.bot.users)}`\n"
                                           f"**Ready for use:** `{self.bot.is_ready()}`\n"
                                           f"**Status:** `{self.bot.activity}`\n"
                                           f"**Heartbeat:** `{round(self.bot.latency, 3)}`\n"
                               )
                 ]
        paginator = BotEmbedPaginator(ctx, embed)
        await paginator.run()

def setup(bot):
    bot.add_cog(Stats(bot))