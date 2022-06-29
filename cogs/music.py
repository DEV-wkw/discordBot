import random
import discord
import youtube_dl
from discord.ext import commands

class music(commands.Cog):
  
  def __init__(self, bot = None):
    self.bot = bot

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    if before.channel == None and after.channel != None:
      await member.voice.channel.connect()
      await member.guild.change_voice_state(channel = member.voice.channel, self_deaf = True)
    elif before.channel != None and after.channel == None:
      await member.guild.voice_client.disconnect()
  
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    channel = await self.bot.fetch_channel(payload.channel_id)
    reaction = await channel.fetch_message(payload.message_id)
    user = await self.bot.fetch_user(payload.user_id)
    if user.id != reaction.author.id:
      if payload.emoji.name == '▶️':
        await music.react(ctx = reaction)
        ctx = await commands.Bot.get_context(self = self.bot, message = reaction)
        input_url = reaction.embeds[0].description
        await self.play(ctx = ctx, input_url = input_url)
      elif payload.emoji.name == '⏸️':
        await music.react(ctx = reaction)
        ctx = await commands.Bot.get_context(self = self.bot, message = reaction)
        ctx.voice_client.stop()
      elif payload.emoji.name == '❎':
        message = await channel.fetch_message(payload.message_id)
        await message.delete()

  @commands.command()
  async def add(self, ctx, input_url):
    await ctx.message.delete()
    if len(input_url) != 43:
      await ctx.send('```The URL is not supported.```', delete_after=3)
    else:
      embed = discord.Embed(
        description = input_url,
        color = discord.Colour.blue()
      )
      embed.set_author(name = 'Added to playlist')
      embed.set_thumbnail(url='https://img.youtube.com/vi/' + input_url[32:43] + '/0.jpg')
      bot_message = await ctx.send(embed = embed)
      await music.react(ctx = bot_message)

  async def play(self, ctx, input_url):
    with youtube_dl.YoutubeDL() as download:
      info = download.extract_info(input_url, download = False)
      source = await discord.FFmpegOpusAudio.from_probe(info['formats'][0]['url'], **{})
      ctx.voice_client.stop()
      ctx.voice_client.play(source)

  @commands.command()
  async def rand(self, ctx):
    await ctx.message.delete()
    rand_music = []
    for channel in ctx.guild.text_channels:
      async for song in channel.history(limit = 20):
        if song.embeds:
          rand_music.append(song)
    await music.play(self, ctx, random.choice(rand_music).embeds[0].description)

  async def react(ctx):
    await ctx.clear_reactions()
    await ctx.add_reaction('▶️')
    await ctx.add_reaction('⏸️')
    await ctx.add_reaction('❎')
        
def setup(c):
  c.add_cog(music(c))