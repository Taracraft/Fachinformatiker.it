# -*- coding: iso-8859-1 -*-
import asyncio
import logging.handlers

from discord import message, Button
from reactionmenu import ReactionMenu
import discord
from reactionmenu.buttons import ButtonType

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.presences = True
client = discord.Client(intents=discord.Intents.all())
g = client.get_guild(1089909008867012701)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='IT-Testbot.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

@client.event
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game('https://www.fachinformatik.it'),
                                     status=discord.Status.online)
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Game('Testbot'), status=discord.Status.online)
        await asyncio.sleep(5)

@client.event
async def on_join(message):
    if message.author.bot:
        return

menu = ReactionMenu(message, back_button='??', next_button='??', config=ReactionMenu.STATIC)
# first and last pages
fpb = Button(emoji='?', linked_to=ButtonType.GO_TO_FIRST_PAGE)
lpb = Button(emoji='?', linked_to=ButtonType.GO_TO_LAST_PAGE)

# go to page
gtpb = Button(emoji='?', linked_to=ButtonType.GO_TO_PAGE)

# end session
esb = Button(emoji='?', linked_to=ButtonType.END_SESSION)

# custom embed
ceb = Button(emoji='?', linked_to=ButtonType.CUSTOM_EMBED, embed=discord.Embed(title='Hello'))

menu.add_button(fpb)
menu.add_button(lpb)
menu.add_button(gtpb)
menu.add_button(esb)
menu.add_button(ceb)
async def main():
    @client.event
    async def on_ready():
        print("Bot is ready!")
        print("Logged in as: " + client.user.name)
        print("Bot ID: " + str(client.user.id))
        for guild in client.guilds:
            print("Connected to server: {}".format(guild))
        print("------")

        print("Starting up...")
        client.loop.create_task(status_task())

if __name__ == '__main__':
    asyncio.run(main())
    client.run('')
