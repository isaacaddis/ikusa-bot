#!/usr/bin/env python
# -*- coding: utf-8 -*-

from discord.ext import commands
from discord import Object
from datetime import datetime
from datetime import timedelta  

import asyncio
import mysql.connector

from helper import Helper

'''
    Bot Config
'''
prefix = "."
bot = commands.Bot(command_prefix=prefix, description='Discord group event scheduler')
h = Helper()

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

'''
Background task

'''

async def background_loop():
    await bot.wait_until_ready()
    #greeting = h.get_random_greeting()
    date_today = datetime.today().strftime('%Y-%m-%d') 
    print("Today is", date_today)
    date_next = datetime.today() + timedelta(days=1)
    date_next = date_next.strftime('%Y-%m-%d')
    channel = bot.get_channel(605574059530649639)
    sql = "SELECT * FROM calendar WHERE d >= %s AND d < %s"
    vals = (date_today,date_next)
    cursor.execute(sql,vals)
    result = cursor.fetchall()
    if result:
        for r in result:
            await channel.send(h.get_random_greeting()+" Letting you know that you're scheduled for event {0} at {1} in timzeone {2}. This message is targeted for users with role {3}.".format(r[2], r[3], r[4], r[5]))
            #print(r)
            #await channel.send(r)
    else:
        await channel.send("You have no events planned within the next three days. TODO: Delete this in production, it would be annoying.")
    asyncio.sleep(86400)

bot.loop.create_task(background_loop()) #initializes background loop as task
bot.run("NjA1NTc3ODMyMTAxNDQ1NzEx.XUEV0w.RV3A5DDWjZDJzknoFoX6L0CJd0k")
