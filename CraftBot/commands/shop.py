from CraftBot.CraftServer import CraftConnector


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
                "---------------------------\n".format(shop_status, shop_location)
    for item in shop_items:
        r_message += (item + "\n")

    await client.send_message(message.author, r_message)


async def shop_add(client, message, param):
    try:
        CraftConnector(message.author).shop_add(param)
    except Exception:
        await client.send_message(message.author, "Invalid Item. Items should follow the pattern:\nT<number> ITEM\n"
                                                  "Example:\nT4 Leather Boots")
        return

    r_message = "{} Added To Your Shop!".format(param)

    await client.send_message(message.author, r_message)

async def shop_remove(client, message, param):
    CraftConnector(message.author).shop_remove(param)

    r_message = "{} Removed From Your Shop!".format(param)

    await client.send_message(message.author, r_message)

async def shop_location_set(client, message, param):
    CraftConnector(message.author).shop_location_set(param)

    r_message = "Shop Location Updated!".format(param)

    await client.send_message(message.author, r_message)

