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
    
class inventory(commands.Cog):

  async def checkPaintbrush(self, ctx, message):
    for key in db.keys():
      if(int(key) == int(ctx.author.id)):
        item_name = db[key][User.item_name.value]
        item_quantity = db[key][User.item_quantity.value]

        color = ""
        msgEnd = ""
        if(item_name == "Red_Paintbrush"):
          color = "diff\n-"
          msgEnd = "-"
        elif(item_name == "Blue_Paintbrush"):
          color = "ini\n["
          msgEnd = "]"
        elif(item_name == "Green_Paintbrush"):
          color = "bash\n\""
          msgEnd = "\""
        elif(item_name == "Yellow_Paintbrush"):
          color = "fix\n"
        else:
          return

        if(item_quantity > 0):
          db[key][User.item_quantity.value] -= 1
          await ctx.message.delete()
          displayMessage = "```" + color + str(message.author)
          displayMessage += ": " + str(message.content) + msgEnd + "```"
          await ctx.send(displayMessage)
      
def setup(c):
  c.add_cog(inventory(c))