#!/usr/bin/env python
# -*- coding: utf-8 -*-
from discord.ext import commands

import mysql.connector
'''
    Bot Config
'''

prefix = "."
bot = commands.Bot(command_prefix=prefix, description='Discord group event scheduler')

'''
    Connect to SQL server
'''

conn = mysql.connector.connect(
       host = "us-cdbr-iron-east-02.cleardb.net", 
       user = "b90bd7aafae0d8",
       password = "bb45d6ec",
       database = "heroku_1492cb9b2e7e903"
        )

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
