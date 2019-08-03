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
cursor = conn.cursor()

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
@bot.command()
async def start(ctx, date, event, t, zone, role):
    sql = "INSERT INTO calendar (d, event, t, zone, role) VALUES (%s, %s, %s, %s, %s)"
    vals = (date, event, t, zone, role)
    cursor.execute(sql, vals)
    conn.commit()
    print("Made reservation for event {0} at {1} for {2} in timezone {3} to members of {4}".format(event, date, t, zone, role))
    await ctx.send("All set! :grinning: You chose to make reservation {0} at {1} for {2} in timezone {3} to members of {4}".format(event, date, t, zone, role))
bot.run("NjA1NTc3ODMyMTAxNDQ1NzEx.XUEV0w.RV3A5DDWjZDJzknoFoX6L0CJd0k")
