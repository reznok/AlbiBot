from CraftBot.CraftServer import CraftConnector

VALID_CITIES = ["caerleon", "bridgewatch", "thetford", "lymhurst", "fort sterling", "martlock"]

async def craft_get_crafters(client, message, param):
    param = param.lower()
    split_param = param.split(" ")
    city = ""
    if split_param[0] == "fort" and split_param[1] == "sterling":
        city += "{} {}".format(split_param[0], split_param[1])
    elif split_param[0] not in VALID_CITIES:
        r_message = "Invalid City Provided. Valid Cities: %s" % ", ".join(VALID_CITIES)
        await client.send_message(message.author, r_message)
        return
    else:
        city = split_param[0]

    item = param.split(city)[1].split(" ", 1)[1]
    print(item)

    crafters = CraftConnector(message.author).crafters_get(city, item)
    if len(crafters) == 0:
        await client.send_message(message.author, "No Crafters Found or Invalid Item")
        return

    r_message = "Online Crafters In {} For {}\n---------------------\n".format(city.title(), item.title())

    for crafter in crafters:
        r_message += crafter + "\n"

    await client.send_message(message.author, r_message)

