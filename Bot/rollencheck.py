# -*- coding: iso-8859-1 -*-
import asyncio
import datetime as datetime
import logging.handlers

import discord
import pytz

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.presences = True
client = discord.Client(intents=intents)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='rollen.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if ("download" in message.content.lower() or "Download" in message.content or "herunterladen" in message.content.lower() or "Herunterladen" in message.content) and ("cloud" in message.content.lower() or "Cloud" in message.content):
        channel = client.get_channel(1091003987089698826)
        target_message = await channel.fetch_message(1103250414931030026)
        await message.channel.send(f"{message.author.mention} Der Download der Cloud ist gesperrt, weitere Informationen unter {target_message.jump_url}")

@client.event
async def check_roles():
        for guild in client.guilds:
            for member in guild.members:
                for role in member.roles:
                    if role.name == "-undefined-":
                        print(
                            f"USER_ID: {member.id:d} - USER_NAME: {member.name}  - ROLE: {role.name} - Beigetreten {member.joined_at.strftime('%d.%m.%Y')}")
                        created = member.joined_at
                        now = datetime.datetime.today().replace(tzinfo=pytz.UTC)
                        join_und_7_tage = created + datetime.timedelta(days=7)
                        if join_und_7_tage < now:
                            print(f"Benutzer gefunden {member.name:s}")
                            userid = member.id
                            getuser = guild.get_member(userid)
                            channel = client.get_channel(1089909009869451277)
                            await channel.send(f"{member.mention} hat die {role.name} Role seit 7 tagen und wird gekickt")
                            embed = discord.Embed(title="Kick",
                                                  description="Du wurdest gekickt weil du keine Rolle in Channel: willkommen ausgewählt hast.",
                                                  color=0xbd2e2e)
                            embed.set_author(name="Fachinformatiker-Discord")
                            embed.add_field(name="Hinweiß",
                                            value="Du kannst wieder joinen, aber wähle eine Rolle innerhalb von 7 Tagen aus. https://discord.gg/AdesPFm2RW",
                                            inline=False)
                            await getuser.send(embed=embed)
                            await getuser.kick(reason='')
        await asyncio.sleep(60 * 60 * 24)

@client.event
async def rolecheck():
    for guild in client.guilds:
        for member in guild.members:
            if member.bot:
                continue  # Überspringe Bots

            rollen = []
            for role in member.roles:
                if role.name.lower() == 'admins' or role.name.lower() == 'moderator' or role.name.lower() == '@everyone' or role.name.lower() == 'server booster':
                    continue  # Ignoriere die Rollen "admins", "moderator", "@everyone" und "server booster"
                rollen.append(role)

            if len(rollen) > 1:  # Überprüfe, ob das Mitglied mehr als eine nicht ignorierte Rolle hat
                undefined = discord.utils.get(member.guild.roles, name="-undefined-")
                await member.remove_roles(undefined)
                for role in rollen:
                    await member.remove_roles(role)
                await member.add_roles(undefined)
                channel = client.get_channel(1089909009869451277)
                await channel.send(f"{member.mention} hat folgende Rollen: {', '.join([r.name for r in rollen])} und wird zu undefined zurückgestuft!")
                print(f"USER_ID: {member.id:d} - USER_NAME: {member.name} - ROLES: {', '.join([r.name for r in rollen])}")
                channel = client.get_channel(1089909009869451274)
                await channel.send(f"{member.mention} du hast mehr als 1 Fachbereich ausgewählt, dir wurden alle Rollen entfernt. Bitte wähle nur 1 Fachbereich aus.")

    await asyncio.sleep(60)  # Eine Wartezeit von 60 Sekunden einfügen

@client.event
async def update_presence():
        await client.change_presence(activity=discord.Game('https://www.fachinformatik.it'), status=discord.Status.online)
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game('Rollen-Check'), status=discord.Status.online)
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
        await client.loop.create_task(update_presence())
        await client.loop.create_task(check_roles())
        await client.loop.create_task(rolecheck())

if __name__ == '__main__':
    asyncio.run(main())
    client.run('')