from discord.ext import commands
import asyncio
import asyncpg
from utils import config
from utils.Db import Db
from utils import cogs

config = config.Config()

async def run():

    login_data = config.dblogin()
    db = await asyncpg.create_pool(**login_data)
    description = config.description()
    bot = Bot(description=description, db=db)

    for query in Db.create_tables():
        await db.execute(query)

    try:
        await bot.start(config.token())
    except Exception as e:
        await db.close()
        await bot.logout()
        print(f"Something went wrong: `{e}`")

"""skidded from ItsVale (https://gist.github.com/itsVale/b63ffca851ab8e645743c45be15cfb60)"""
class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=commands.when_mentioned_or(config.prefix()),
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

loop = asyncio.get_event_loop()
loop.run_until_complete(run())