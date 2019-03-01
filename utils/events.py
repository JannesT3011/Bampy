from discord.ext import commands

class Events:
    def __init__(self, bot):
        self.bot = bot

    async def on_guild_join(self, guild):
        """
        Bot join event

        INSERT THE DEFAULT DATA INTO THE DATABASE + SEND THE ´GET STARTED´ MESSAGE TO THE SERVER OWNER
        """
        query = """INSERT INTO setup(server_id, userjoin_leave, servertags, modlog, meme, counter, mod, games, nsfw, edu, social) 
        VALUES ($1, false, true, false, true, false, true, true, true, true, true);
        """
        await self.bot.db.execute(query, guild.id)
        print(True)


def setup(bot):
    bot.add_cog(Events(bot))