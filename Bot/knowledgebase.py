# -*- coding: iso-8859-1 -*-
import asyncio
import logging.handlers
import requests
import discord
from discord.ui import Button, View
import json
import os

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

# Config

# Variablen
bot_token = ''
api_key = ''
kb_channel_id = '1272239238708199434'
guild_id = '1089909008867012701'
token_file = 'token.json'

# URL der REST API
documents_url = f'https://api.bnder.net/consumer/v1/guilds/{guild_id}/documents'
document_url_template = 'https://api.bnder.net/consumer/v1/guilds/{guild_id}/documents/{document_id}'
token_refresh_url = 'https://api.bnder.net/consumer/v1/auth/refresh'  # Ersetze durch den tatsächlichen Token-Refresh-Endpoint

# Funktion zum Laden des Tokens aus der Datei
def load_token():
    if os.path.exists(token_file):
        with open(token_file, 'r') as file:
            data = json.load(file)
            return data.get('access_token')
    return None

# Funktion zum Speichern des Tokens in der Datei
def save_token(token):
    with open(token_file, 'w') as file:
        json.dump({'access_token': token}, file)

# Funktion zum Aktualisieren des API-Tokens
def refresh_api_token():
    global headers
    response = requests.post(token_refresh_url, headers={'Authorization': f'Bearer {api_key}'})
    if response.status_code == 200:
        new_token = response.json().get('access_token')
        if new_token:
            headers['Authorization'] = f'Bearer {new_token}'
            save_token(new_token)
            return True
    print("Fehler beim Aktualisieren des Tokens:", response.status_code, response.text)
    return False

# Token aus der Datei laden und in den Header integrieren
token = load_token()
if token:
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Fachinformatik.IT Discord Anfrage'
    }
else:
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'Fachinformatik.IT Discord Anfrage'
    }

# Funktion zur Durchführung der GET-Anfrage für alle Dokumente
def get_all_documents(limit=100, project_id=None):
    params = {
        'limit': str(limit)
    }
    if project_id:
        params['project_id'] = project_id

    response = requests.get(documents_url, headers=headers, params=params)
    if response.status_code == 401:  # Unauthorized, Token möglicherweise abgelaufen
        if refresh_api_token():
            response = requests.get(documents_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get('documents', [])
    else:
        print(f"Fehler: {response.status_code}")
        print("Antwort:", response.text)
        return None

# Funktion zur Durchführung der GET-Anfrage für ein einzelnes Dokument
def get_document_details(document_id):
    url = document_url_template.format(guild_id=guild_id, document_id=document_id)
    response = requests.get(url, headers=headers)
    if response.status_code == 401:  # Unauthorized, Token möglicherweise abgelaufen
        if refresh_api_token():
            response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler: {response.status_code}")
        print("Antwort:", response.text)
        return None

# Funktion zum Erstellen von Discord-Embeds aus Dokumenten
def create_embed_from_document(document, content=None):
    embed = discord.Embed(
        title=document.get('title', 'Kein Titel'),
        description=content or 'Klicke auf Ausklappen, um den Inhalt anzuzeigen.',
        color=discord.Color.blue()  # Farbe des Embeds
    )
    return embed

# Funktion zum Erstellen des Buttons
class DetailsButtonView(View):
    def __init__(self, document_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document_id = document_id
        self.showing_content = False
        self.timeout = 600  # Setze den Timeout für die View (600 Sekunden = 10 Minuten)

    @discord.ui.button(label="Ausklappen", style=discord.ButtonStyle.primary)
    async def details_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.showing_content:
            # Inhalt ausblenden
            document = get_document_details(self.document_id)
            if document:
                embed = create_embed_from_document(document)
                await interaction.response.edit_message(embed=embed, view=self)
                self.showing_content = False
        else:
            # Inhalt anzeigen
            document = get_document_details(self.document_id)
            if document:
                content = document.get('content', 'Kein Inhalt verfügbar')
                embed = create_embed_from_document(document, content=content)
                await interaction.response.edit_message(embed=embed, view=self)
                self.showing_content = True

# Funktion zum Senden der Dokumente an den Discord-Kanal
async def send_documents_to_channel(channel, documents):
    if not documents:
        await channel.send("Keine Dokumente gefunden.")
        return

    for document in documents:
        embed = create_embed_from_document(document)
        view = DetailsButtonView(document_id=document['id'])
        await channel.send(embed=embed, view=view)

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
