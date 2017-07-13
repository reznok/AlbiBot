import datetime

async def utc(client, message):
        await client.send_message(message.channel, "UTC Time: %s on %s" % (datetime.datetime.utcnow().strftime("%H:%M:%S"),
                                                                           datetime.datetime.utcnow().strftime("%D")))
