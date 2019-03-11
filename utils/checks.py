from . import ON, OFF
from discord.ext import commands

class Checks:
    def __init__(self, bot, guild, row):
        self.bot = bot
        self.guild = guild
        self.row = row

    def setup(self, pos:str):
        """
        CHECK IF THE SETUP FUNCTION IS TRUE OR FALSE
        """
        if self.row[pos] == True:
            return ON
        else:
            return OFF