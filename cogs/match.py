# Matches Cog
# Status: fix offset to add all previous offsets as well

from discord.ext import commands
import discord
import aiosqlite
import aiohttp
import clipboard
 

class Match(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.args = [1, 2]
        self.args_english = "1 or 2"
        self.name = "Match History"
        self.msg = "**Example**: `s!matches obsidian_mb 5`"
        self.url = "https://surviv.io/api/match_history"
        self.headers = {"content-type": "application/json; charset=UTF-8"}

    async def check_valid_players(self, player: str):
        """ Checks if a player is valid """
        url = "https://surviv.io/api/user_stats"
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = {"slug": f"{player}", "interval": "all", "mapIdFilter": "-1"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as r:
                    c = await r.json()
        except:
            print("Connection Error")
        print(c)
        return c if not c else True

    @commands.Cog.listener()
    async def on_ready(self):
        print("Match History Cog Loaded")
    

    @commands.command(aliases=["matches", "match_history"])
    async def match(self, ctx):
        id = ctx.message.guild.id
        conn = await aiosqlite.connect("servers.db")
        c = await conn.cursor()
        await c.execute("select prefix from servers where name = ?", [str(id)])
        prefix = await c.fetchall()
        prefix = prefix[0][0]
        args = ctx.message.content.split()
        arg_count = len(args) - 1
        msg = f"**Argument #1**: Player Name \n**Argument #2** (optional): Amount of matches to return \n**Example**: `{prefix}match obsidian_mb 5` (last 5 games of obsidian_mb)\n**NOTE**: You must put in the **user's account name** which might differ with their in game name."
        if arg_count not in self.args:
            await ctx.send(
                f"**{self.name}** command only takes an argument count of **{self.args_english}**\n{msg}"
            )

        else:
            player_name = args[1]
            last_ngames = int(args[2]) if len(args) > 2 else 10
            # Need to make it so that can grab all the games
            if last_ngames < 0:
                await ctx.send("I can't retrieve a negative amount of games")
            else:
                lowered = player_name.lower()
                offset = ((last_ngames - 1) // 10) * 10
                previous_offsets = [i for i in range(0, offset) if not i % 10]
                await ctx.send(previous_offsets)
                await ctx.send(offset)
                data = {
                    "slug": f"{lowered}",
                    "offset": f"{offset}",
                    "count": f"{last_ngames - offset}",
                    "teamModeFilter": "7",
                }
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            self.url, headers=self.headers, json=data
                        ) as r:
                            c = await r.json()
                except:
                    await ctx.send(
                        "Connection Error. Please log an **issue description** of this with the **issue command**."
                    )
                if not await self.check_valid_players(lowered):
                    embed = discord.Embed(
                        description=f"**{player_name}** is not a valid player of surviv.io.",
                        color=0x00B037,
                    )
                    await ctx.send(embed=embed)
                elif c == []:
                    desc = f"**{player_name}** doesn't have any recent games"
                    embed = discord.Embed(description=desc, color=0x00B037)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Recent Games Available")
                    modes = ["Solo", "Duos", "Squads"]
                    for game in c:
                        team_mode = modes[game["team_mode"] - 1]
                        time_alive = divmod(int(game["time_alive"]), 60)
                        rank = game["rank"]
                        kills = game["kills"]
                        desc = ''
                        title = f"{player_name}'s Last __{last_ngames}__ games"
                        embed = discord.Embed(title=title, description=desc)
                        await ctx.send(embed=embed)
                  

def setup(bot):
    bot.add_cog(Match(bot))
