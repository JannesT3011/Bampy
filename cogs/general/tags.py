from discord.ext import commands
from utils.colors import random_color
import discord
from utils.config import Config
from utils.errors import NameTooLongError, TagNotFoundError, NoServerTags, TagExists

def is_enabled():
    """CHECK IF COMMAND IS ENABLED"""
    async def pred(ctx):
        query = """SELECT servertags FROM setup WHERE server_id = $1;"""
        row = await ctx.bot.db.fetch(query, ctx.guild.id)
        return row[0]["servertags"] is True

    return commands.check(pred)

class Servertags:
    def __init__(self, bot):
        self.bot = bot
        #print(__class__.__name__.lower())

    @commands.group(name="tag",aliases=["tags"], invoke_without_command=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @is_enabled()
    async def _tag(self, ctx, *, name:str):
        """GET A TAG BY NAME"""
        try:
            query = """SELECT * FROM tags WHERE name = $1 AND server_id = $2;"""
            row = await self.bot.db.fetchrow(query, name, ctx.guild.id)
            await ctx.send(row["text"])
        except TypeError:
            raise TagNotFoundError(name)

    @_tag.error
    async def on_error(self, ctx, error):
        if isinstance(error, TagNotFoundError):
            embed = discord.Embed(title="Oops..", color=random_color(), description=f"`{error}` isn't a tag on this server")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Oh.. you missed an argument...", color=random_color(), description=f"Type `{Config().prefix()}tag <TAGNAME>`")
            await ctx.send(embed=embed)

    @_tag.command(name="all", aliases=["list", "show_all"])
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @is_enabled()
    async def _tag_all(self, ctx):
        """GET ALL SEVER TAGS"""
        query = """SELECT name FROM tags 
                WHERE server_id = $1;
                """
        tags = [tag[0] for tag in await self.bot.db.fetch(query, ctx.guild.id)]
        if len(tags) is 0:
            raise NoServerTags

        embed = discord.Embed(title="All available server tags:\n"f"`{Config().prefix()}tag <NAME>`",color=random_color(),description=f"```css\n{', '.join(tags)}\n```")
        embed.set_author(name=f"{ctx.guild.name} ~ Tags", icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @_tag_all.error
    async def on_error(self, ctx, error):
        """ERROR HANDLING FOR _tag FUNCTION"""
        if isinstance(error, NoServerTags):
            embed = discord.Embed(title="Oh, sorry..", description="There are no tags on this server", color=random_color())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(title="Oh..", color=random_color(), description="You can't use this command, because it's disabled\n"f"Type `{Config().prefix()}setup enable tags`")
            await ctx.send(embed=embed)

    @_tag.command(name="add", aliases=["create"])
    @commands.cooldown(1, 10.0, commands.BucketType.user)
    @is_enabled()
    async def _tag_add(self, ctx, name:str, *, text:str):
        """ADD A NEW TAG"""
        if len(name) > 50:
            raise NameTooLongError
        query = """SELECT name FROM tags WHERE server_id = $1;"""
        tags = [tag[0] for tag in await self.bot.db.fetch(query, ctx.guild.id)]
        if name in tags:
            raise TagExists
        query = """INSERT INTO tags(server_id, name, text, author) VALUES ($1, $2, $3, $4);"""
        await self.bot.db.execute(query, ctx.guild.id, name, text, ctx.author.id)
        embed = discord.Embed(title="Yeahhh", description="Tag successfully created\n"f"**Name: **`{name}`\n"f"**Author: **`{ctx.author.name}`")
        await ctx.send(embed=embed)

    @_tag_add.error
    async def on_error(self, ctx, error):
        """ERROR HANDLING FOR _tag_edit FUNCTION"""
        if isinstance(error, TagExists):
            embed = discord.Embed(title="Oops.. sorry", color=random_color(), description="This tag is already registered")
            await ctx.send(embed=embed)
        elif isinstance(error, NameTooLongError):
            embed = discord.Embed(title="Oops..", color=random_color(), description="The tag name is to long\n""A tag name can only be 50 characters long!")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(title="Oh..", color=random_color(), description="You can't use this command, because it's disabled\n"f"Type `{Config().prefix()}setup enable tags`")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Oops..", color=random_color(), description="You forgot some important arguments!\n""Use it like this: \n"f"`{Config().prefix()}tag add <TAGNAME> <TEXT>`")
            await ctx.send(embed=embed)

    @_tag.command(name="delete", aliases=["del", "drop"])
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @is_enabled()
    async def _tag_delete(self, ctx, *,name:str):
        """DELETE A TAG"""
        query = """SELECT * FROM tags WHERE server_id = $1 AND name = $2 AND author = $3;"""
        row = await self.bot.db.fetchrow(query, ctx.guild.id, name, ctx.author.id)
        if row is None:
            raise TagNotFoundError(name)
        if ctx.author.id is ctx.guild.owner_id:
            del_query = """DELETE FROM tags WHERE server_id = $1 AND name = $2;"""
            await self.bot.db.execute(del_query, ctx.guild.id, name)
            embed = discord.Embed(title="Okayyy..", color=random_color(),description=f"You deleted `{name}` successfully")
            await ctx.send(embed=embed)
        else:
            del_query = """DELETE FROM tags WHERE server_id = $1 AND name = $2 and author = $3;"""
            await self.bot.db.execute(del_query, ctx.guild.id, name, ctx.author.id)
            embed = discord.Embed(title="Okayyy..", color=random_color(), description=f"You deleted `{name}` successfully")
            await ctx.send(embed=embed)

    @_tag_delete.error
    async def on_error(self, ctx, error):
        """ERROR HANDLING FOR _tag_delete FUNCTION"""
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Oops..", color=random_color(),description="You forgot some important arguments!\n""Use it like this: \n"f"`{Config().prefix()}tag delete <TAGNAME>`")
            await ctx.send(embed=embed)
        elif isinstance(error, TagNotFoundError):
            embed = discord.Embed(title="Oops..", color=random_color(), description=f"`{error}` isn't a tag on this server")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(title="Oh..", color=random_color(), description="You can't use this command, because it's disabled\n"f"Type `{Config().prefix()}setup enable tags`")
            await ctx.send(embed=embed)

    @_tag.command(name="my", aliases=["mytags"])
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @is_enabled()
    async def _tag_mytags(self, ctx):
        """SHOWS THE TAGS YOU CREATED"""
        query = """SELECT name FROM tags WHERE server_id = $1 AND author = $2;"""
        tags = [tag[0] for tag in await self.bot.db.fetch(query, ctx.guild.id, ctx.author.id)]
        if len(tags) is 0:
            raise NoServerTags
        embed = discord.Embed(title="Your server tags:", description=f"```css\n {', '.join(tags)}\n ```")
        embed.set_author(name=f"{ctx.author.name} ~ tags", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @_tag_mytags.error
    async def on_error(self, ctx, error):
        """ERROR HANDLING FOR _tag_mytags FUNCTION"""
        if isinstance(error, NoServerTags):
            embed = discord.Embed(title="Oops..", color=random_color(), description="It seems like you haven't created a server tags yet\n"f"`{Config().prefix()}tag add <NAME> <TEXT>`")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(title="Oh..", color=random_color(), description="You can't use this command, because it's disabled\n"f"Type `{Config().prefix()}setup enable tags`")
            await ctx.send(embed=embed)

    @_tag.command(name="edit")
    @commands.cooldown(1, 10.0, commands.BucketType.user)
    @is_enabled()
    async def _tag_edit(self, ctx, name, *, new_text:str):
        """UPDATE AN EXISTING TAG"""
        try:
            query = """SELECT * FROM tags WHERE name = $1 AND server_id = $2 AND author = $3;"""
            await self.bot.db.fetchrow(query, name, ctx.guild.id, ctx.author.id)
            update_query = """UPDATE tags SET text = $1 WHERE name = $2 AND server_id = $3 AND author = $4;"""
            await self.bot.db.execute(update_query, new_text, name, ctx.guild.id, ctx.author.id)
            embed = discord.Embed(title="Yeeeees", color=random_color(), description="You updated the tag!")
            await ctx.send(embed=embed)
        except TypeError:
            raise TagNotFoundError(name)

    @_tag_edit.error
    async def on_error(self, ctx, error):
        """ERROR HANDLING FOR _tag_edit FUNCTION"""
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Oops..", color=random_color(),description="You forgot some important arguments!\n""Use it like this: \n"f"`{Config().prefix()}tag edit <TAGNAME> <NEW TAG TEXT>`")
            await ctx.send(embed=embed)
        elif isinstance(error, TagNotFoundError):
            embed = discord.Embed(title="Oops..", color=random_color(), description=f"`{error}` isn't a tag on this server")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(title="Oh..", color=random_color(), description="You can't use this command, because it's disabled\n"f"Type `{Config().prefix()}setup enable tags`")
            await ctx.send(embed=embed)

    """TAG INFO ~ COMING SOON"""



def setup(bot):
    bot.add_cog(Servertags(bot))