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
    filename='IT-Statistik.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate durch 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

channel_id = '1107024792399396976'  # Die ID des Channels "mitglieder"


@client.event
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game('https://www.fachinformatik.it'),
                                     status=discord.Status.online)
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Game('Daten sammeln...'), status=discord.Status.online)
        await asyncio.sleep(5)


@client.event
async def on_guild_member_add(member):
    await update_channel_name()


@client.event
async def on_guild_member_remove(member):
    await update_channel_name()



client.event
async def update_channel_name():
    guild = client.get_guild(1089909008867012701)
    if guild is None:
        print("Guild not found")
        return

    channel = guild.get_channel(int(channel_id))
    if channel is None:
        print("Channel not found")
        return

    member_count = guild.member_count
    new_channel_name = f' Mitglieder: {member_count}'

    if channel.name != new_channel_name:
        await channel.edit(name=new_channel_name)
        print(f"Channel name updated to: {new_channel_name}")

client.event
async def update_channel_name_loop():
    while True:
        await update_channel_name()
        await asyncio.sleep(300)  # Warte 5 Minuten


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
    client.run('')
