import discord
import json
# Commands #

from commands.utc import utc
from commands.wiki import wiki

BOT_ABOUT = """
```
Written By: Reznok#1688 (Discord)
---------------------------------
AlbiBot is a Discord bot built for Albion Online.
Currently in development. For feature requests, ping me on Discord!
Check AlbiBot out on GitHub:
https://github.com/reznok/AlbiBot
```
"""

BOT_HELP = """
```
AlbiBot by Reznok#1688 (Discord)
----------------------------------------------------
!utc                    | Display UTC Time
!wiki <search>          | Get Wiki Page For an Item
!about                  | About AlbiBot
```
"""


config = json.loads(open('config.json').read())  # Load Configs
client = discord.Client()


def is_admin(author):
    """
    Is this user a bot admin?
    :param author: message.author
    :return: bool
    """
    if str(author).lower() in config["admins"]:
        return True
    return False


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!utc'):
        print("UTC | " + str(message.author) + " | " + message.content)
        await utc(client, message)

    if message.content.startswith('!wiki'):
        print("Wiki | " + str(message.author) + " | " + message.content)
        await wiki(client, message)

    if message.content.startswith('!about'):
        print("About | " + str(message.author) + " | " + message.content)
        await client.send_message(message.channel, BOT_ABOUT)

    if message.content.startswith('!help'):
        print("Help | " + str(message.author) + " | " + message.content)
        await client.send_message(message.channel, BOT_HELP)

client.run(config["discord_token"])
