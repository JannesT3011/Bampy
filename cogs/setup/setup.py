from discord.ext import commands
from utils.colors import random_color
import discord
from disputils import BotEmbedPaginator
from utils.config import Config
from . import checks

class Setup:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="setup", aliases=["settings", "options"])
    @commands.has_permissions(manage_guild=True)
    async def _setup(self, ctx):
        """Configure the bot"""
        query = """SELECT * FROM setup WHERE server_id = $1;"""
        row = await self.bot.db.fetchrow(query, ctx.guild.id)
        CHECK = checks.Checks(self.bot, ctx.guild.id, row)
        embed = [discord.Embed(title=f"All available setup functions - More info's: `{Config().prefix()}setup <FUNCTION/NUMBER>`", color=random_color(),
        description="**1. `user_join_leave` : `Enable/disable the bot message, when a user joins/leave`**\n"
                    "**2. `tags` : `Enable/disable server tags`**\n"
                    "**3. `modlog` : `Enable/disable the modolg channel`**\n"
                    "**4. `meme` : `Enable/disable meme comamnd/channel`**\n"
                    "**5. `counter` : `Enable/disable the counterchannel`**\n"
                    "**6. `mod` : `Enable/disable moderating stuff`**\n"
                    "~~**7. `games` : `Enable/disable games`**~~\n"
                    "~~**8. `nsfw` : `Enable/disable nsfw stuff`**~~\n"
                    "**9. `edu` : `Enable/disable education stuff`**\n"
                    "~~**10. `social` : `Enable/disable social media stuff`**~~\n")
                    .set_author(icon_url=ctx.guild.icon_url, name=f"{ctx.guild.name} ~ Setup"),
        discord.Embed(title=f"Setup on {ctx.guild.name}", color=random_color(),
                      description=f"**1. `user_join_leave` : {CHECK.setup('userjoin_leave')}**\n"
                                  f"**2. `tags` : {CHECK.setup('servertags')}**\n"
                                  f"**3. `modlog` : {CHECK.setup('modlog')}**\n"
                                  f"**4. `meme` : {CHECK.setup('meme')}**\n"
                                  f"**5. `counter` : {CHECK.setup('counter')}**\n"
                                  f"**6. `mod` : {CHECK.setup('mod')}**\n"
                                  f"~~**7. `games` : {CHECK.setup('games')}**~~\n"
                                  f"~~**8. `nsfw` : {CHECK.setup('nsfw')}**~~\n"
                                  f"**9. `edu` : {CHECK.setup('edu')}**\n"
                                  f"~~**10. `social` : {CHECK.setup('social')}**~~\n")
                 ]
        paginator = BotEmbedPaginator(ctx, embed)
        await paginator.run()


def setup(bot):
    bot.add_cog(Setup(bot))