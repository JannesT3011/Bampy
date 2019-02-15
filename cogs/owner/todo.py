from discord.ext import commands
from utils.colors import random_color
from discord import Embed
class Todo:
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="todo")
    async def _todo(self, ctx, *, text:str=None):
        """Add something as ToDo"""
        if text:
            file = open("./cogs/owner/Todo.txt", "a", encoding="utf-8")
            file.write(f"\n {text}")
            file.close()
            embed = Embed(title="Add a new ToDo:", description="```css\n"f"{text}\n""```", color=random_color())
            await ctx.send(embed=embed)
        else:
            file = open("./cogs/owner/Todo.txt", "r", encoding="utf-8").read()
            embed = Embed(title="ToDo's", description="```css\n"f"{file}\n""```", color=random_color())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Todo(bot))