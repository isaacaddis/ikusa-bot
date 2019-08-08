#!/usr/bin/env python
# -*- coding: utf-8 -*-

from discord.ext import commands
from discord import (utils, Object, Embed)

from datetime import datetime
from datetime import timedelta  

import asyncio
import mysql.connector

from helper import Helper
import secret

'''
    Bot Config
'''

prefix = "."
CHANNEL_ID = 608048185037946883
bot = commands.Bot(command_prefix=prefix, description='Discord group event scheduler')
bot.remove_command("help")
h = Helper()

'''
    Connect to SQL server (config for your own DB)
'''

conn = mysql.connector.connect(
       host = "us-cdbr-iron-east-02.cleardb.net", 
       user = "b90bd7aafae0d8",
       password = secret.PASSWORD,
       database = "heroku_1492cb9b2e7e903"
        )
cursor = conn.cursor()

@bot.event
async def on_ready():
    print("Initalized Ikusa bot.")

@bot.command()
async def ping(ctx):
    await ctx.send(bot.latency)

@bot.event
async def on_message(message):
    if message.content.startswith('ikusa config'):
        channel = message.channel
        author = message.author
        def check(ms):
            return (ms.channel == channel and ms.author == author)
        await message.channel.send("I'm here! Start off by telling me what date your event will take place. (YY-MM-DD)")
        date = (await bot.wait_for("message",check=check)).content
        await channel.send("Okay, I've got you scheduled for {0}".format(date))
        await channel.send("Next, tell me the name of your event.")
        event = (await bot.wait_for("message",check=check)).content
        await channel.send("Event name '{0}'? Got it.".format(event))
        await channel.send("Now, tell me what time the event will take place. (HH:MM:SS)")
        t = (await bot.wait_for("message",check=check)).content
        await channel.send("What timezone is {0} configured for? (Example: GMT-7)".format(t))
        zone = (await bot.wait_for("message",check=check)).content
        await channel.send("Lastly, tell me who you want to send this to. You can get the ID of a role or channel by entering '\\@role' or '\\#channel' (without the quotes).")
        role = (await bot.wait_for("message",check=check)).content
        sql = "INSERT INTO calendar (d, event, t, zone, role) VALUES (%s, %s, %s, %s, %s)"
        vals = (date, event, t, zone, role)
        cursor.execute(sql,vals)
        embed = Embed(title = "Ikusa [Bot]", color=0xe87400)
        embed.add_field(name="All set!", value = "You chose to make reservation '{0}' at {1} for {2}     in timezone {3} to members of {4}".format(event, date, t, zone, role))
        msg = await channel.send(embed=embed)

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
    embed = Embed(title = "Ikusa [Bot]", color=0xe87400)
    embed.add_field(name="All set!", value = "You chose to make reservation '{0}' at {1} for {2}     in timezone {3} to members of {4}".format(event, date, t, zone, role))
    msg = await channel.send(embed=embed)
    await msg.add_reaction(emoji="\u2705")

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
        embed = Embed(title = "Ikusa [Bot]", color=0xe87400)
        for r in result:
            role_id = h.remove_whitespace(r[5]) #in this format: <@&603172759115399169>
            embed.add_field(name = "Scheduled: {0}".format(r[2]), value = "{0} Letting you know that you're scheduled for event {1} at {2} in timzeone {3}. This message is targeted for users with role {4}.".format(h.get_random_greeting(),r[2],r[3], r[4], role_id))
            print("Role ID: {0}".format(role_id))
            await channel.send(embed=embed)
    asyncio.sleep(86400)

'''
    Custom help command
'''

@bot.command(pass_context=True)
async def help(ctx):
    embed = Embed(title = "Ikusa [Bot]", color=0xe87400)
    embed.add_field(name="Usage", value="You can use Ikusa with one .start command or by sending 'ikusa config' (without quotes)")
    embed.add_field(name=".start", value="Call .start like this: .start 2019-08-12 hangout 12:30:00 GMT-7 Splatoon2. This will mention users with role or in channel 'Splatoon2' for event 'hangout' for August 12, 2019 at 12:30. You MUST use this format or your scheduling will not work correctly. ")
    embed.add_field(name="ikusa config", value="This method will require you to input the data as shown above, but in a step-by-step manner with directions, as opposed to a single-step command. You can also use multi-word event names with this method (commands treat space-delimited words as individual arguments)")
    await ctx.send(embed=embed)
    
bot.loop.create_task(background_loop())
bot.run(secret.TOKEN)  # EDIT THIS FOR CUSTOM USE
