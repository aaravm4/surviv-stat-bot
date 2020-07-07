# Main file for bot
# edit everything that has a fixed prefix

import discord
from discord.ext import commands
import os
import aiosqlite

async def get_pref(bot, msg):
  name = msg.guild.id
  conn = await aiosqlite.connect('servers.db')
  c = await conn.cursor()
  await c.execute('select prefix from servers where name = ?', [str(name)])
  cor_fetch = await c.fetchall()
  prefix = cor_fetch[0][0]
  return prefix

bot = commands.Bot(command_prefix = get_pref)

@bot.event
async def on_ready():
  print('Bot Is Running ...')
  conn = await aiosqlite.connect('servers.db')
  c = await conn.cursor()
  await c.execute('''CREATE TABLE IF NOT EXISTS SERVERS(
                NAME TEXT,
                CHANGER TEXT,
                PREFIX TEXT,
                CONFIG TEXT,
                CHANGER2 TEXT,
                GEN BOOL
                 )''')
  await conn.commit()
  current_servers = [str(server.id) for server in bot.guilds]
  print(f'Bot is Running on {len(current_servers)}!')
  await c.execute('select name from servers')
  d = await c.fetchall()
  e = [i[0] for i in d]
  print(e)
  for s in current_servers:
    if s not in e:
      await c.execute("insert into servers values (?, 'None', 's!', '', 'None', 1)", [str(s)])
      await conn.commit()
  for old in e:
    if old not in current_servers:
      await c.execute('delete from servers where name = ?', [str(old)])
      await conn.commit()
  game = discord.Game("Type s!help")
  await bot.change_presence(activity=game)
  

@bot.event
async def on_guild_join(guild):
    # Inserts Values into the Server for info
    print(f'Bot was added to {guild} :)')
    conn = await aiosqlite.connect('servers.db')
    c = await conn.cursor()
    await c.execute('select name from servers')
    await c.execute("insert into servers values (?, 'None', 's!', '', 'None', 1)", [str(guild.id)])
    await conn.commit()


@bot.event
async def on_guild_remove(guild):
  print(f'Bot was removed from {guild} :(')
  # Removing that guild from table
  conn = await aiosqlite.connect('servers.db')
  c = await conn.cursor()
  id = guild.id
  await c.execute('delete from servers where name = ?', [str(id)])
  await conn.commit()


  
dont_load = []
# Loading All Cogs
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
      if file not in dont_load:
        bot.load_extension(f'cogs.{file[:-3]}')

    
bot.run('NjU1NTQxODcxMDA2ODQyODkx.XwSdDg.byq8kSKiccNpjtXaRf9xgdHptm4')


### 
#| Add Link Gen Command
###
