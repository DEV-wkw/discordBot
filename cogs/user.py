import os
import time
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
    
class user(commands.Cog):
  
  @commands.command()
  async def info(self, ctx):
    await ctx.message.delete()
    await user.addNewUser(self, ctx)
    for key in db.keys():
      if(int(key) == int(ctx.author.id)):
        xpBar = ''
        for i in range(10):
          if((db[key][User.xp.value]%50)/5 >= i+1):
            xpBar += '🟩'
          else:
            xpBar += '⬜'
        embed = discord.Embed(
          description = xpBar + '\n```XP: ' + str(db[key][User.xp.value]) + '```',
          color = discord.Colour.gold()
        )
        embed.set_author(name = db[key][User.name.value] + ' (Lv.' + str(int(db[key][User.xp.value]/50)) + ')')
        embed.set_thumbnail(url = db[key][User.avatar_url.value])
        await ctx.send(embed = embed, delete_after=30)
          
  async def addNewUser(self, ctx):
    userFound = False
    for key in db.keys():
      if(int(key) == int(ctx.author.id)):
        userFound = True
    if(not userFound):
      db[ctx.author.id] = [
        f"{ctx.author.id}",
        f"{ctx.author.name}",
        f"{ctx.author.avatar_url}",
        0,
        int(time.time())
      ]
      await ctx.send('```Welcome! New user ' + str(ctx.author.name) + '.```', delete_after=30)
      await user.info(self, ctx)

  async def addXp(self, ctx, amount):
    for key in db.keys():
      if(int(key) == int(ctx.author.id)):
        xpInterval = int(time.time()) - int(db[key][User.xp_time.value])
        if(xpInterval > int(os.getenv('xp_time_token'))):
          levelBefore = int(db[key][User.xp.value]/50)
          db[key][User.xp.value] = int(db[key][User.xp.value]) + int(amount)
          db[key][User.xp_time.value] = int(time.time())
          levelAfter = int(db[key][User.xp.value]/50)
          if(levelBefore != levelAfter):
            await ctx.send('```Congratulations! User ' + str(ctx.author.name) + ' level up to Lv.' + str(levelAfter) + '```', delete_after=30)
            await user.info(self, ctx)
      
def setup(c):
  c.add_cog(user(c))