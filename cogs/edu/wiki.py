import wikipedia
from discord.ext import commands
from utils import colors
import discord

class Wiki:
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="wiki")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _wiki(self, ctx, *, word:str):
        """Search something on Wikipedia"""
        if " " in word:
            word_split = word.split(" ")
            new_word = word_split[0] + word_split[1]
            text = wikipedia.summary(new_word, sentences=2)
            embed = discord.Embed(
                title=f"WikiSearch ~ `{new_word}`",
                description=f"```{text}```",
                url=f"https://wikipedia.org/wiki/{new_word}",
                color=int(colors.random_color())
            )
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            text = wikipedia.summary(word, sentences=2)
            embed = discord.Embed(
                title=f"WikiSearch ~ `{word}`",
                description=f"```{text}```",
                url=f"https://wikipedia.org/wiki/{word}",
                color=int(colors.random_color())
            )
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @_wiki.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(
                title="Cant find this word!",
                description="Try another one\n"
                            "Maybe try to to write them together.",
                color=int(colors.random_color())
            )
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Wiki(bot))
