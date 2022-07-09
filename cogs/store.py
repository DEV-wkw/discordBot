import os
import discord
from enum import Enum
from replit import db
from discord.ext import commands

class User(Enum):
  id = 0
  name = 1
  avatar_url = 2
  xp = 3
  xp_time = 4
  item_name = 5
  item_quantity = 6
    
class store(commands.Cog):
  
  @commands.command()
  async def store(self, ctx):
    await ctx.message.delete()
    embed = discord.Embed(
      description = '\n```   Red_Paintbrush: 20XP (x5)\n  Blue_Paintbrush: 20XP (x5)\n Green_Paintbrush: 20XP (x5)\nYellow_Paintbrush: 20XP (x5)' + '```',
      color = discord.Colour.gold()
    )
    embed.set_author(name = 'XP Store')
    await ctx.send(embed = embed, delete_after=30)

  @commands.command()
  async def buy(self, ctx, item):
    for key in db.keys():
      if(int(key) == int(ctx.author.id)):
        if(item != "Red_Paintbrush" and item != "Blue_Paintbrush" and item != "Green_Paintbrush" and item != "Yellow_Paintbrush"):
          await ctx.send('```Item not found.```', delete_after=30)
          return
        if(db[key][User.xp.value] < 20):
          await ctx.send('```You don\'t have enough XP.```', delete_after=30)
          return
        db[key][User.xp.value] = int(db[key][User.xp.value]) - 20
        db[key][User.item_name.value] = item
        db[key][User.item_quantity.value] = 5
        await ctx.send('```Purchased ' + item + ' successfully.' + '```', delete_after=30)
          
      
def setup(c):
  c.add_cog(store(c))