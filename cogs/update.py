# Update Cog
# STATUS: done

import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup as soupify
import aiosqlite


class Update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = "Update"
        self.args = 0
        self.url = "http://surviv.io/"
        self.msg = "**Example**: `s!update`"

    @commands.Cog.listener()
    async def on_ready(self):
        print("Update Cog Loaded")

    @commands.command(aliases=["releases", "release", "updates", "new"])
    async def update(self, ctx):
        id = ctx.message.guild.id
        conn = await aiosqlite.connect("servers.db")
        c = await conn.cursor()
        await c.execute("select prefix from servers where name = ?", [str(id)])
        prefix = await c.fetchall()
        prefix = prefix[0][0]
        msg = f"**Example**: `{prefix}update`"
        args = ctx.message.content.split()
        arg_count = len(args) - 1
        if arg_count != self.args:
            await ctx.send(
                f"**{self.name}** command only takes an argument count of **{self.args}** \n{msg}"
            )
        else:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.url) as r:
                        raw = await r.read()
            except:
                ctx.send(
                    "Failed to connect to surviv.io website. Log an issue with the issue command"
                )
            html = soupify(raw, "html.parser")
            news_wrapper = html.find("div", {"id": "news-current"})
            date = news_wrapper.find("small").text
            title = news_wrapper.find("strong").text
            title = f"⏫ {title} ({date}) ⏫"
            desc = news_wrapper.findAll("p")[1].text
            print(title)
            print(desc)
            embed = discord.Embed(title=title, description=desc, color=0x00B037)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Update(bot))
