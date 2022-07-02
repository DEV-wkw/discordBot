import os
import discord
from discord.ext import commands
from extension import extension_host

c = commands.Bot(command_prefix = '')

@c.event
async def on_ready():
  print('program started')

@c.event
async def on_message(message):
  if(int(message.author.id) != int(os.getenv('bot_id_token'))):
    ctx = await c.get_context(message)
    user = c.get_cog('user')
    await user.addNewUser(ctx)
    await user.addXp(ctx, 3)
    await c.process_commands(message)
    
for file in os.listdir('./cogs'):
  if file.endswith('.py'):
    c.load_extension(f'cogs.{file[:-3]}')

extension_host()
c.run(os.getenv('discord_token'))