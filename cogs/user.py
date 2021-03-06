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
    item_id = 5
    item_quantity = 6


class user(commands.Cog):
    itemList = []
    itemList.append([0, "paintRed", 20, 5])
    itemList.append([1, "paintBlue", 20, 5])
    itemList.append([2, "paintGreen", 20, 5])
    itemList.append([3, "paintYellow", 20, 5])
    itemList.append([4, "paintOrange", 20, 5])

    @commands.command()
    async def info(self, ctx):
        await user.addNewUser(self, ctx)
        for key in db.keys():
            if (int(key) == int(ctx.author.id)):
                xpBar = "```"
                for i in range(10):
                    if ((db[key][User.xp.value] % 50) / 5 >= i + 1):
                        xpBar += "🟨"
                    else:
                        xpBar += "⬜"
                embed = discord.Embed(
                    description="**" + db[key][User.name.value] + " (Lv." +
                    str(int(db[key][User.xp.value] / 50)) + ")**" + xpBar +
                    "````⭐ " + str(db[key][User.xp.value]) + "`\n`🎁 " +
                    str(user.itemList[db[key][User.item_id.value]][1]) +
                    " (x" + str(db[key][User.item_quantity.value]) + ")`" + "",
                    color=discord.Colour.gold())
                embed.set_thumbnail(url=db[key][User.avatar_url.value])
                await ctx.send(embed=embed, delete_after=30)

    async def addNewUser(self, ctx):
        userFound = False
        for key in db.keys():
            if (int(key) == int(ctx.author.id)):
                userFound = True
        if (not userFound):
            db[ctx.author.id] = [
                f"{ctx.author.id}", f"{ctx.author.name}",
                f"{ctx.author.avatar_url}", 0,
                int(time.time()), "None", 0
            ]
            await ctx.send("```Welcome! New user " + str(ctx.author.name) +
                           ".```",
                           delete_after=30)
            await user.info(self, ctx)
        else:
            for key in db.keys():
                if (int(key) == int(ctx.author.id)):
                    userData = db[key]
                    if (len(userData) < 7):
                        for i in range(len(userData), 7):
                            db[key].append("")

    async def addXp(self, ctx, amount):
        for key in db.keys():
            if (int(key) == int(ctx.author.id)):
                xpInterval = int(time.time()) - int(
                    db[key][User.xp_time.value])
                if (xpInterval > int(os.getenv("xp_time_token"))):
                    levelBefore = int(db[key][User.xp.value] / 50)
                    db[key][User.xp.value] = int(
                        db[key][User.xp.value]) + int(amount)
                    db[key][User.xp_time.value] = int(time.time())
                    levelAfter = int(db[key][User.xp.value] / 50)
                    if (levelBefore != levelAfter):
                        await ctx.send("```Congratulations! User " +
                                       str(ctx.author.name) +
                                       " level up to Lv." + str(levelAfter) +
                                       "```",
                                       delete_after=30)
                        await user.info(self, ctx)


def setup(c):
    c.add_cog(user(c))