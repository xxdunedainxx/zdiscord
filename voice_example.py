import discord
from discord.ext import commands
import time
import asyncio

bot = commands.Bot(command_prefix = "!")

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.command()
async def q5(ctx):
    await ctx.send("@here QUEUE STARTING IN 5 MINUTES")

@bot.command()
async def q3(ctx):
    await ctx.send("@here QUEUE STARTING IN 3 MINUTES")

@bot.command()
async def q1(ctx):
    await ctx.send("@here QUEUE STARTING IN 1 MINUTES")

@bot.command()
async def ping(ctx):
    ping_ = bot.latency
    ping =  round(ping_ * 1000)
    await ctx.send(f"my ping is {ping}ms")

@bot.command()
async def startq(ctx):
    voicechannel = discord.utils.get(ctx.guild.channels, name='Team Rheem')
    vc = await voicechannel.connect()
    bot.run('NzA4NTI5ODA2NTc2MTg5NDkw.XrYsnA.Z__XlHMY7vh2AipQpjVw3T0meWM')

startq()