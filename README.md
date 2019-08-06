# Ikusa

A simple-to-use and simple-to-maintain flexible Python bot for Discord.

## Requirements

+ Python 3 (3.6.8)
+ Discord.py

### Usage

Clone the repository and replace the bot token and channel ID with those that pertain to your needs. It is recommended to create a seperate channel for scheduling to improve visibility to group members. 

Run the bot by simply running `python ikusa.py`. 

Ikusa is currently command-based only. 

The main command is `.start` and it takes several arguments, with the format:

.start (date) (event) (time) (timezone) (role)

Here is an example command:

```
.start 2019-08-06 hangout 01:35:00 gmt-7 <@&608041105207853133>
```

Because Ikusa parses each space-delimited word as a new argument, there is currently no support for multi-word event names. You can get the role or channel ID you want to input as the last argument (the group to mention during event notifications) by setting up Developer Mode within your Discord client and entering "\@role" or "\#channel" as a message for roles and channels, respectively. 

### Notifications

Ikusa will check its records once a day for any events scheduled for the next three days. It will mention the supplied role/channel. In the main ikusa.py file


### Privacy 

Ikusa is meant to be installed and configured locally. The bot does not collect user data.
