from discord.ext import commands
from utils.colors import random_color
import discord

class Setup:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="setup", aliases=["settings", "options"])
    @commands.has_permissions(manage_guild=True)
    async def _setup(self, ctx):
        embed = discord.Embed(title="All available setup functions - More info's: `b.setup <FUNCTION/NUMBER>`", color=random_color(),
        description="**1. `user_join_leave` : `Enable/disable the bot message, when a user joins/leave`**\n"
                    "**2. `tags` : `Enable/disable server tags`**\n"
                    "**3. `modlog` : `Enable/disable the modolg channel`**\n"
                    "**4. `meme` : `Enable/disable meme comamnd/channel`**\n"
                    "**5. `counter` : `Enable/disable the counterchannel`**\n"
                    "**6. `mod` : `Enable/disable moderating stuff`**\n"
                    "~~**7. `games` : `Enable/disable games`**~~\n"
                    "~~**8. `nsfw` : `Enable/disable nsfw stuff`**~~\n"
                    "**9. `edu` : `Enable/disable education stuff`**\n"
                    "~~**10. `social` : `Enable/disable social media stuff`**~~\n"
                              )
        embed.set_author(icon_url=ctx.guild.icon_url, name=f"{ctx.guild.name} ~ Setup")
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name.split('#')[0]}")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Setup(bot))