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
    item_id = 5
    item_quantity = 6

class inventory(commands.Cog):
    async def checkItems(self, ctx, message):
        for key in db.keys():
            if (int(key) == int(ctx.author.id)):
                item_id = db[key][User.item_id.value]
                item_quantity = db[key][User.item_quantity.value]

                color = ""
                msgEnd = ""
                if (item_id == 0):
                    color = "diff\n-"
                    msgEnd = "-"
                elif (item_id == 1):
                    color = "ini\n["
                    msgEnd = "]"
                elif (item_id == 2):
                    color = "bash\n\""
                    msgEnd = "\""
                elif (item_id == 3):
                    color = "fix\n"
                elif (item_id == 4):
                    color = "css\n["
                    msgEnd = "]"
                else:
                    return

                if (message.embeds):
                    url = message.embeds[0].url
                    message.content = message.content.replace(url, "")
                    if (message.content == ""):
                        message.content = "sent a video "

                if (item_quantity > 0):
                    db[key][User.item_quantity.value] -= 1
                    await ctx.message.delete()
                    displayMessage = "```" + color + str(message.author)
                    displayMessage += ": " + str(
                        message.content) + msgEnd + "```"
                    await ctx.send(displayMessage)
                    if (message.embeds):
                        await ctx.send(url)


def setup(c):
    c.add_cog(inventory(c))