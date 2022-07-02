import discord
from discord.ext import commands

class chat(commands.Cog):

  def __init__(self, bot = None):
    self.bot = bot

  @commands.command()
  async def clear(self, ctx):
    await ctx.channel.purge(limit = 20, check = lambda x: not x.embeds)
    await ctx.send('```20 messages has been deleted.```', delete_after=3)
    user = self.bot.get_cog('database')
    await user.addXp(ctx, 3)

  @commands.command()
  async def hide(self, ctx, message):
    await ctx.message.delete()
    await ctx.send(message)
      
def setup(c):
  c.add_cog(chat(c))