import discord
from utils.colors import random_color

class GetStartd(discord.Embed):
    def __init__(self):
        super().__init__(
            title="Bampy ~ Get started",
            description="Hello! My name is Bampy and I was coded to HELP YOU!!!!!!\n""Before you use me, just take a look at this few notes",
            color=random_color()
        )
        GetStartd.add_field(self, name="Use b.setup to configure me (This is not required)", value="E.g: `b.setup games true`\n""b.setup shows you all configure options", inline=False)
        GetStartd.add_field(self, name="You can set your own server prefix", value="Type `b.prefix <PREFIX>` to set a new prefix\n""__NOTE:__ Only one prefix per server")
        GetStartd.add_field(self, name="Help - see all commands", value="Type: `b.help`", inline=False)
        GetStartd.set_footer(self, text="💓 Have fun 💓")