import dbl
import discord
from discord.ext import commands
import json

dbl_token = json.load(open("token.json", "r"))["dbl_token"]


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = dbl_token
        self.dblpy = dbl.DBLClient(
            self.bot, self.token, autopost=True
        )  # Autopost will post your guild count every 30 minutes

    async def on_guild_post():
        print("Server count posted successfully")


def setup(bot):
    bot.add_cog(TopGG(bot))
