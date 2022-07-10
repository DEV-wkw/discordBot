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

  itemList = []
  itemList.append(["Red_Paintbrush", 20, 5])
  itemList.append(["Blue_Paintbrush", 20, 5])
  itemList.append(["Green_Paintbrush", 20, 5])
  itemList.append(["Yellow_Paintbrush", 20, 5])
  
  @commands.command()
  async def store(self, ctx):
    content = ""
    for i in range(len(store.itemList)):
      content += str(store.itemList[i][0]).rjust(18) + ": "
      content += str(store.itemList[i][1]).rjust(3) + "XP(x"
      content += str(store.itemList[i][2]).rjust(2,"0") + ")\n"
    
    embed = discord.Embed(
      description = "\n```" + content + "```",
      color = discord.Colour.gold()
    )
    embed.set_author(name = "XP Store")
    await ctx.send(embed = embed, delete_after=30)

  @commands.command()
  async def buy(self, ctx, itemName):
    for i in range(len(store.itemList)):
      if (store.itemList[i][0] == itemName):
        item = store.itemList[i]
        break
      elif (i == len(store.itemList) - 1):
        await ctx.send("```Item not found.```", delete_after=30)
        return
        
    for key in db.keys():
      if(int(key) == int(ctx.author.id)):
        if(db[key][User.xp.value] < item[1]):
          await ctx.send("```You don\"t have enough XP.```", delete_after=30)
          return
          
        db[key][User.item_name.value] = item[0]
        db[key][User.xp.value] = int(db[key][User.xp.value]) - item[1]
        db[key][User.item_quantity.value] = item[2]
        await ctx.send("```Purchased " + item[0] + " (x" + str(item[2]) + ")" + " successfully." + "```", delete_after=30)
      
def setup(c):
  c.add_cog(store(c))