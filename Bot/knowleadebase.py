# -*- coding: iso-8859-1 -*-
import asyncio
import logging.handlers
import requests
import discord

# Intents
intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.presences = True
client = discord.Client(intents=intents)

# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='knowledgebase.py.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate durch 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Variablen
bot_token = ''
api_key = ''
termin_channel_id = '1272232640702844949'
task_channel_id = '1272232677134696589'
kb_channel_id = '1272239238708199434'
guild_id = '1089909008867012701'

# URL der REST API
url = f'https://api.bnder.net/consumer/v1/guilds/{guild_id}/documents'

# HTTP-Header
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}',
    'User-Agent': 'YOUR_USER_AGENT'
}

# Funktion zur Durchführung der GET-Anfrage
def get_all_documents(limit=100, project_id=None):
    params = {
        'limit': str(limit)
    }
    if project_id:
        params['project_id'] = project_id

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get('documents', [])
    else:
        print(f"Fehler: {response.status_code}")
        print("Antwort:", response.text)
        return None

# Funktion zum Senden der Dokumente an den Discord-Kanal
async def send_documents_to_channel(channel, documents):
    if not documents:
        await channel.send("Keine Dokumente gefunden.")
        return

    for document in documents:
        await channel.send(f"Dokument: {document}")

# Funktion zum Leeren des Kanals
async def purge_channel(channel):
    print("Channel wird geleert")
    await channel.purge()
    print("Channel wurde geleert")

# Discord-Bot-Ereignisse
@client.event
async def on_ready():
    print("Bot is ready!")
    print("Logged in as: " + client.user.name)
    print("Bot ID: " + str(client.user.id))
    for guild in client.guilds:
        print("Connected to server: {}".format(guild))
    print("------")
    print("Starting up...")

    # Leere den KB-Kanal
    guild = client.get_guild(int(guild_id))
    if guild:
        kb_channel = guild.get_channel(int(kb_channel_id))
        if kb_channel:
            await purge_channel(kb_channel)

            documents = get_all_documents(limit=100)
            if documents is not None:
                await send_documents_to_channel(kb_channel, documents)
    client.loop.create_task(status_task())

# Status Task
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game('https://www.fachinformatik.it'), status=discord.Status.online)
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Game('KB wird erschaffen...'), status=discord.Status.online)
        await asyncio.sleep(5)

# Main
async def main():
    await client.start(bot_token)

if __name__ == '__main__':
    asyncio.run(main())
