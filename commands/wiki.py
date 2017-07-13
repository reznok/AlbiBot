import string
import requests

async def wiki(client, message):
    query = message.content.split("!wiki ")[1]
    r = requests.get("http://albiononline.wikia.com/wiki/Special:Search?search=%s&fulltext=Search&ns0=1&ns14=1#" % query)
    if r.status_code != 200:
        await client.send_message(message.channel, "Error Connecting to Wiki")
        return

    try:
        result = r.text.split('<li class="result">')[1].split('href="')[1].split('"')[0]
    except Exception:
        await client.send_message(message.channel, "Error With Query")
        return

    await client.send_message(message.channel, "*Results Will Be Weird Until Wiki is Finished* \n" + result)
