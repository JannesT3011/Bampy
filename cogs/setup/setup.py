from discord.ext import commands
from utils.colors import random_color
import discord
from disputils import BotEmbedPaginator
from utils.config import Config
from . import checks, SETUP_OPTIONS
import pprint

class Setup:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="setup", aliases=["settings", "options"], invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def _setup(self, ctx):
        """Configure the bot"""
        query = """SELECT * FROM setup WHERE server_id = $1;"""
        row = await self.bot.db.fetchrow(query, ctx.guild.id)
        CHECK = checks.Checks(self.bot, ctx.guild.id, row)
        embed = [discord.Embed(title=f"All available setup functions - More info's: `{Config().prefix()}setup <enable/disable> <FUNCTION>`", color=random_color(),
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

    @_setup.command(name="enable")
    @commands.has_permissions(manage_guild=True)
    async def _setup_enable(self, ctx, *, arg:str):
        """ENABLE A SETUP FUNCTION"""

        if arg in SETUP_OPTIONS:
            await self._update_db(arg, True, ctx.guild)
            embed = discord.Embed(title="Yeaahhh", color=random_color(), description=f"You enabled `{arg}`")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Oops..", color=random_color(), description="This isn't a setup function...\n\n"f"`{', '.join(SETUP_OPTIONS)}`")
            await ctx.send(embed=embed)

    @_setup.command(name="disable")
    @commands.has_permissions(manage_guild=True)
    async def _setup_disable(self, ctx, *, arg:str):
        if arg in SETUP_OPTIONS:
            await self._update_db(arg, False, ctx.guild)
            embed = discord.Embed(title="Okayy", color=random_color(), description=f"You disabled {arg}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Oops..", color=random_color(),description="This isn't a setup function...\n\n"f"`{', '.join(SETUP_OPTIONS)}`")
            await ctx.send(embed=embed)


    async def _update_db(self, arg:str, set:bool, guild):
        ALIASES = {
            "user_join_leave": """UPDATE setup SET userjoin_leave = $1 WHERE server_id = $2;""",
            "tags": """UPDATE setup SET servertags = $1 WHERE server_id = $2;""",
            "modlog": """UPDATE setup SET modlog = $1 WHERE server_id = $2;""",
            "meme": """UPDATE setup SET meme = $1 WHERE server_id = $2;""",
            "count": """UPDATE setup SET counter = $1 WHERE server_id = $2;""",
            "mod": """UPDATE setup SET mod = $1 WHERE server_id = $2;""",
            "games": """UPDATE setup SET games = $1 WHERE server_id = $2;""",
            "nsfw": """UPDATE setup SET nsfw = $1 WHERE server_id = $2;""",
            "edu": """UPDATE setup SET edu = $1 WHERE server_id = $2;""",
            "social": """UPDATE setup SET social = $1 WHERE server_id = $2;"""
        }
        await self.bot.db.execute(ALIASES[arg], set, guild.id)



def setup(bot):
    bot.add_cog(Setup(bot))