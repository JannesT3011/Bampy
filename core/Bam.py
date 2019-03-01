from discord.ext import commands
import asyncpg
from utils import config
from utils.DB.Db import Db
from utils import cogs
import discord

config = config.Config()

async def get_prefix(bot, message):
    try:
        query = """SELECT * FROM general WHERE id = $1;"""
        row = await bot.db.fetchrow(query, message.guild.id)
    except AttributeError:
        pass

    if not message.guild:
        return commands.when_mentioned_or(config.prefix())(bot, message)

    if row is None:
        query = """INSERT INTO general (id, prefix) VALUES ($1, $2)"""
        await bot.db.execute(query, message.guild.id, config.prefix())
        return commands.when_mentioned_or(config.prefix())(bot, message)

    return commands.when_mentioned_or(row["prefix"], config.prefix())(bot, message)

async def run():

    login_data = config.dblogin()
    db = await asyncpg.create_pool(**login_data)
    description = config.description()
    bot = Bampy(description=description, db=db)

    for query in Db.create_tables():
        await db.execute(query)

    try:
        await bot.start(config.token())
    except Exception as e:
        await db.close()
        await bot.logout()
        print(f"Something went wrong: `{e}`")

"""skidded from ItsVale (https://gist.github.com/itsVale/b63ffca851ab8e645743c45be15cfb60)"""
class Bampy(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=get_prefix,
            description=kwargs.pop("description")
        )
        self.db = kwargs.pop("db")

        for ext in cogs.extensions:
            try:
                self.load_extension(ext)
            except Exception as e:
                print(f"Cant load {ext}")
                raise e

    async def on_ready(self):
        print("##########\n"f"{self.user.name}\n"f"{self.user.id}\n""##########")
        print(discord.utils.oauth_url(self.user.id))
