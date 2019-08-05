#!/usr/bin/env python
# -*- coding: utf-8 -*-

from discord.ext import commands
from discord import Object
from discord import utils

from datetime import datetime
from datetime import timedelta  

import asyncio
import mysql.connector

from helper import Helper

'''
    Bot Config
'''
prefix = "."
CHANNEL_ID = 605574059530649639
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
    print("Initalized Ikusa bot.")

@bot.command()
async def ping(ctx):
    await ctx.send(bot.latency)

'''
    Main command
    Params: date (YY-MM-DD) (str), event (str), t (str), zone (str), role (str)
'''

@bot.command(pass_context=True)
async def start(ctx, date, event, t, zone, role):
    sql = "INSERT INTO calendar (d, event, t, zone, role) VALUES (%s, %s, %s, %s, %s)"
    vals = (date, event, t, zone, role)
    cursor.execute(sql, vals)
    conn.commit()
    print("Made reservation for event {0} at {1} for {2} in timezone {3} to members of {4}".format(event, date, t, zone, role))
    channel = bot.get_channel(CHANNEL_ID)
    msg = await channel.send("All set! :grinning: You chose to make reservation '{0}' at {1} for {2} in timezone {3} to members of {4}".format(event, date, t, zone, role))
    await msg.add_reaction(emoji="\N{GRINNING FACE}")
    '''
    cache_msg = utils.get(bot.messages, id = msg.id)
    for reactor in cache_msg.reactions:
        reactors = await bot.get_reaction_users(reactor)
        for member in reactors:
            print("Member: {0}".format(member))
            await channel.send(member.name)
    '''
    

'''
Background task - checks for scheduled events in the next 3 days
Loops every 24 hours (86400 seconds)
'''

async def background_loop():
    await bot.wait_until_ready()
    date_today = datetime.today().strftime('%Y-%m-%d') 
    date_next = datetime.today() + timedelta(days=2)
    date_next = date_next.strftime('%Y-%m-%d')
    channel = bot.get_channel(CHANNEL_ID)
    sql = "SELECT * FROM calendar WHERE d >= %s AND d < %s"
    vals = (date_today,date_next)
    cursor.execute(sql,vals)
    result = cursor.fetchall()
    if result:
        for r in result:
            role_id = h.remove_whitespace(r[5]) #in this format: <@&603172759115399169>
            print("Role ID: {0}".format(role_id))
            await channel.send("{0} Letting you know that you're scheduled for event {1} at {2} in timzeone {3}. This message is targeted for users with role {4}.".format(h.get_random_greeting(),r[2], r[3], r[4], role_id))
    else:
        await channel.send("You have no events planned within the next three days. TODO: Delete this in production, it would be annoying.")
    asyncio.sleep(86400)

bot.loop.create_task(background_loop()) #initializes background loop as task
bot.run("NjA1NTc3ODMyMTAxNDQ1NzEx.XUEV0w.RV3A5DDWjZDJzknoFoX6L0CJd0k")
