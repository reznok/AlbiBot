import datetime

async def utc(client, message):
        await client.send_message(message.channel, "UTC Time: " + datetime.datetime.utcnow().strftime("%H:%M:%S"))
