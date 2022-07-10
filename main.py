import os
import discord
from discord.ext import commands
from extension import extension_host

c = commands.Bot(command_prefix = "")

@c.event
async def on_ready():
  print("program started")
  await c.change_presence(activity = discord.Game(name = "type \"help\" for info"))

@c.event
async def on_message(message):
  commandList = ["help", "info", "clear", "add", "rand", "buy", "store"]
  
  if(int(message.author.id) != int(os.getenv("bot_id_token"))):
    ctx = await c.get_context(message)
    user = c.get_cog("user")
    inventory = c.get_cog("inventory")

    if(message.content.split()[0] in commandList):
      await ctx.message.delete()
      await ctx.send("```▸ " + message.content + "```", delete_after=30)
      await c.process_commands(message)
    else:
      await user.addNewUser(ctx)
      await user.addXp(ctx, 3)
      await c.process_commands(message)
      await inventory.checkPaintbrush(ctx, message)

c.remove_command("help")
@c.command()
async def help(ctx):
  content = ""
  content += " info        - show user info\n"
  content += "clear        - clear latest 20 messages\n"
  content += "  add (URL)  - add music\n"
  content += " rand        - play music randomly\n"
  content += "  buy (item) - buy items\n"
  content += "store        - open store\n"
  embed = discord.Embed(
      description = "\n```" + content + "```",
      color = discord.Colour.gold()
    )
  embed.set_author(name = "Commands Available")
  await ctx.send(embed = embed, delete_after=30)
    
for file in os.listdir("./cogs"):
  if file.endswith(".py"):
    c.load_extension(f"cogs.{file[:-3]}")

extension_host()
c.run(os.getenv("discord_token"))