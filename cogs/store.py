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

class store(commands.Cog):
    itemList = []
    itemList.append([1, "paintBlue", 12, 5])
    itemList.append([4, "paintOrange", 12, 5])
    itemList.append([0, "paintRed     [SOLD]", 0, 0])
    itemList.append([2, "paintGreen   [SOLD]", 0, 0])
    itemList.append([3, "paintYellow", 12, 5])
    itemList_id = 0
    itemList_name = 1
    itemList_xp = 2
    itemList_quantity = 3

    @commands.command()
    async def store(self, ctx):
        content = ""
        balance = "`XP: " + str(db[str(ctx.author.id)][User.xp.value])
        for i in range(len(store.itemList)):
            content += str(i + 1) + ". "
            content += str(
                store.itemList[i][store.itemList_name]).ljust(20) + "⭐ "
            content += str(store.itemList[i][store.itemList_xp]).rjust(
                2, "0") + " (x"
            content += str(store.itemList[i][store.itemList_quantity]).rjust(
                2, "0") + ")\n"

        embed = discord.Embed(description=balance + "`\n```" + content + "```",
                              color=discord.Colour.gold())
        embed.set_author(name=ctx.author.name + "'s XP Store")
        await ctx.send(embed=embed, delete_after=30)

    @commands.command()
    async def buy(self, ctx, itemName):
        for i in range(len(store.itemList)):
            if (store.itemList[i][store.itemList_name] == itemName
                    and store.itemList[i][store.itemList_xp] != 0
                    and store.itemList[i][store.itemList_quantity] != 0):
                item = store.itemList[i]
                break
            elif (i == len(store.itemList) - 1):
                await ctx.send("```Item not found.```", delete_after=30)
                return

        for key in db.keys():
            if (int(key) == int(ctx.author.id)):
                if (db[key][User.xp.value] < item[store.itemList_xp]):
                    await ctx.send("```You don\"t have enough XP.```",
                                   delete_after=30)
                    return

                db[key][User.item_id.value] = item[store.itemList_id]
                db[key][User.xp.value] = int(
                    db[key][User.xp.value]) - item[store.itemList_xp]
                db[key][User.item_quantity.value] = item[
                    store.itemList_quantity]
                await ctx.send("```Purchased " + item[store.itemList_name] +
                               " (x" + str(item[store.itemList_quantity]) +
                               ")" + " successfully." + "```",
                               delete_after=30)


def setup(c):
    c.add_cog(store(c))