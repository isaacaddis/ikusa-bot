#!/usr/bin/env python
# -*- coding: utf-8 -*-
from discord.ext import commands
prefix = "."
bot = commands.Bot(command_prefix=prefix, description='Discord group event scheduler')

@bot.event
async def on_ready():
    print("Howdy.")
'''
@bot.event
async def on_message(message):
    pass
'''
@bot.command()
async def ping(ctx):
    await ctx.send(bot.latency)

bot.run("NjA1NTc3ODMyMTAxNDQ1NzEx.XUEV0w.RV3A5DDWjZDJzknoFoX6L0CJd0k")
