import discord
import json
# Commands #

from commands.utc import utc
from commands.wiki import wiki
from CraftBot.commands.shop import *
from CraftBot.commands.craft import *

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

For Crafters
----------------------------------------------------
!shop                       | Lists your shop
!shopitems                  | List all items you can add to your shop
!shopadd <item>             | Add an item you can craft
!shopremove <item>          | Remove an item from shop
!shoplocation <city>        | Set what city you are based out of
!shoponline                 | Flag yourself as online. You will receive crafting requests
!shopoffline                | Flag yourself as offline

For Shoppers
-----------------------------------------------------
!craft <city> <item>           | Connect with someone that can craft

Item Format: <tier> <item>

Examples
----------
T4 Mage Helmet
T5.1 Knight Boots
T3 Warbow

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

    if message.content == '!shop':
        print("Shop | " + str(message.author) + " | " + message.content)
        await shop_get(client, message, message.content.split("!shop")[1])

    if message.content == '!shoponline':
        print("Shop | " + str(message.author) + " | " + message.content)
        await shop_online(client, message, 1)

    if message.content == '!shopoffline':
        print("Shop | " + str(message.author) + " | " + message.content)
        await shop_online(client, message, 0)

    if message.content.startswith('!shopadd '):
        print("Shop Add | " + str(message.author) + " | " + message.content)
        await shop_add(client, message, message.content.split("!shopadd ")[1])

    if message.content.startswith('!shopremove '):
        print("Shop Remove | " + str(message.author) + " | " + message.content)
        await shop_remove(client, message, message.content.split("!shopremove ")[1])

    if message.content.startswith('!shoplocation '):
        print("Shop Remove | " + str(message.author) + " | " + message.content)
        await shop_location_set(client, message, message.content.split("!shoplocation ")[1])
    if message.content.startswith('!craft '):
        print("Craft | " + str(message.author) + " | " + message.content)
        await craft_get_crafters(client, message, message.content.split("!craft ")[1])

client.run(config["discord_token"])
