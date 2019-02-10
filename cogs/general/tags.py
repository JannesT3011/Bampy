from discord.ext import commands
from utils import colors
import discord

class Tag:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="createtag", aliases=["ct", "tagcreate"])
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def _create(self, ctx, name:str,*, content:str):
        """Create a new tag"""
        query = """INSERT INTO tags
                   VALUES ($1, $2, $3)
        """
        await self.bot.db.execute(query, name, ctx.author.id, content)
        embed = discord.Embed(title="Tag created successfully!", description=f"See the tag, by using b.loadtag {name}", color=colors.random_color())
        await ctx.send(embed=embed)

    @commands.command(name="loadtag", aliases=["lt", "tag"])
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def _load(self, ctx, name:str):
        """Load a tag!"""
        query = """SELECT * FROM tags WHERE tag = $1"""
        row = await self.bot.db.fetchrow(query, name)
        await ctx.send(row['text'])

    @_load.error
    async def on_error(self, ctx,error):
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(title="Cant find this tag!", color=colors.random_color())
            await ctx.send(embed=embed)

    @commands.command(name="deltag", aliases=["dt", "deletetag"]) # check if author is author of tag
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def _delete(self, ctx, name:str):
        """Delete a tag!"""
        query = """DELETE FROM tags WHERE tag = $1"""
        _query = """SELECT * FROM tags WHERE tag = $1"""
        row = await self.bot.db.fetchrow(_query, name)
        if row["id"] == ctx.author.id:
            await self.bot.db.execute(query, name)
            embed = discord.Embed(title="Tag successful deleted!", color=colors.random_color())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="You cant delete this tag!", color=colors.random_color(), description="You are not the author of this tag!")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Tag(bot))