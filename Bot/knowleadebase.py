# -*- coding: iso-8859-1 -*-
import asyncio
import logging.handlers
import discord

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.presences = True
client = discord.Client(intents=intents)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='knowleadebase.py.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate durch 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)


#Variabeln
bot_token=''
api_key = ''
termin_channel_id = '1272232640702844949'  # Die ID des Channels "Termine"
task_channel_id = '1272232677134696589'  # Die ID des Channels "Task"
kb_channel_id = '1272239238708199434'  # Die ID des Channels "Knowleadebase"


@client.event
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game('https://www.fachinformatik.it'),
                                     status=discord.Status.online)
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Game('KB wird erschaffen...'), status=discord.Status.online)
        await asyncio.sleep(5)


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
        client.loop.create_task(update_channel_name_loop())
        client.loop.create_task(status_task())


if __name__ == '__main__':
    asyncio.run(main())
    client.run(bot_token)
