import os
import discord
from discord.ext import commands
from extension import extension_host

c = commands.Bot(command_prefix = '')

@c.event
async def on_ready():
  print('program started')
    
for file in os.listdir('./cogs'):
  if file.endswith('.py'):
    c.load_extension(f'cogs.{file[:-3]}')

extension_host()
c.run(os.getenv('discord_token'))