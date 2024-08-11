# -*- coding: iso-8859-1 -*-
import asyncio
import logging.handlers
import discord
from discord.utils import get

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
    filename='fi-reg.log',
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
        await client.change_presence(activity=discord.Game('Registrieren...'), status=discord.Status.online)
        await asyncio.sleep(5)


@client.event
async def on_member_join(member: discord.Member):
    role = discord.utils.get(member.guild.roles, name="Mitglieder")
    await member.add_roles(role)
    channel = client.get_channel(1089909009869451277)
    await channel.send(f"{member.mention} hat die {role.name} Role zugewiesen bekommen, und wurde per DM begrüßt")
    embed = discord.Embed(title="Willkommen auf dem Fachinformatiker Discord.",
                          description="Wichtige Infos für die Benutzung des Discord.", color=0x8b6f6f)
    embed.add_field(name="Bitte die Regeln lesen!",
                    value="Bei nicht einhaltung behalten wir uns dass Recht bei, zu kicken und auch zu bannen. Bei Fragen können wir jederzeit helfen.",
                    inline=False)
    embed.set_footer(text="by Thomas(Taracraft#0762)")
    await member.send(embed=embed)


def main():
    @client.event
    async def on_ready():
        global g
        print("Bot is ready!")
        print("Logged in as: " + client.user.name)
        print("Bot ID: " + str(client.user.id))
        for guild in client.guilds:
            print("Connected to server: {}".format(guild))
        print("------")
        client.loop.create_task(status_task())


if __name__ == '__main__':
    main()

client.run('')
