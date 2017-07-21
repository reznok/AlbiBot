from CraftBot.CraftServer import CraftConnector

VALID_CITIES = ["caerleon", "bridgewatch", "thetford", "lymhurst", "fort sterling", "martlock"]


async def shop_get(client, message, param):
    cc = CraftConnector(message.author)
    shop_items = cc.shop_get()
    shop_location = cc.shop_location_get()
    shop_status = cc.shop_status_get()

    if shop_status == 1:
        shop_status = "ONLINE"
    else:
        shop_status = "OFFLINE"

    r_message = "Shop Status: {}\nShop Location: {}\n\nCraftables\n" \
                "---------------------------\n".format(shop_status, shop_location.title())
    for item in shop_items:
        r_message += (item.title() + "\n")

    await client.send_message(message.author, r_message)


async def shop_add(client, message, param):
    try:
        CraftConnector(message.author).shop_add(param.lower())
    except Exception:
        await client.send_message(message.author, "Invalid Item. Use !help to see valid item pattern.")
        return

    r_message = "{} Added To Your Shop!".format(param.title())

    await client.send_message(message.author, r_message)

async def shop_remove(client, message, param):
    CraftConnector(message.author).shop_remove(param)

    r_message = "{} Removed From Your Shop!".format(param.title())

    await client.send_message(message.author, r_message)

async def shop_location_set(client, message, param):
    if not CraftConnector(message.author).shop_location_set(param):
        r_message = "Invalid City Provided. Valid Cities: %s" % ", ".join(VALID_CITIES)

    else:
        r_message = "Shop Location Updated!".format(param)

    await client.send_message(message.author, r_message)


async def shop_online(client, message, param):
    CraftConnector(message.author).shop_set_online(param)

    if param == 0:
        r_message = "Your Shop Is Now Offline"

    elif param == 1:
        r_message = "Your Shop Is Now Online"

    else:
        r_message = "You Broke Something, Nice!"

    await client.send_message(message.author, r_message)
    return



