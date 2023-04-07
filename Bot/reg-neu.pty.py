# -*- coding: iso-8859-1 -*-
import asyncio
import logging.handlers

import discord
from discord.utils import get

'''rolelist = [1089909009248698481,
            1089909009248698479,
            1089909009248698480,
            1089909008867012708,
            1089909008867012703,
            1089909008867012702,
            1089909008867012705,
            1089909008867012704,
            1093651596585484369,
            1093652255783264347]'''
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
    filename='discord.log',
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
async def on_member_join(member: discord.Member):
    role = discord.utils.get(member.guild.roles, name="-undefined-")
    await member.add_roles(role)
    channel = client.get_channel(1092355243418861619)
    await channel.send(f"{member.mention} hat die {role.name} Role zugewiesen bekommen, und wurde per DM begrüßt")
    embed = discord.Embed(title="Willkommen auf dem Fachinformatiker Discord.",
                          description="Wichtige Infos für die Benutzung des Discord.", color=0x8b6f6f)
    embed.add_field(name="Bitte wähle in #willkommenn-welcome __Eine__ Fachrichtung!",
                    value="Falls du dies nicht innerhalb von 7 Tagen dies machst, wirst du Entfernt.", inline=False)
    embed.add_field(name="Eine Neuer Join ist jedoch möglich.",
                    value="Für weitere Fragen zögere nicht die Admins zu Kontaktieren", inline=False)
    embed.set_footer(text="by Thomas(Taracraft#0762)")
    await member.send(embed=embed)


# Assign the role when the role is added as a reaction to the message.
@client.event
async def on_raw_reaction_add(payload):
    guild = client.get_guild(payload.guild_id)
    member = get(guild.members, id=payload.user_id)
    undefined = discord.utils.get(member.guild.roles, name="-undefined-")
    # channel and message IDs should be integer:
    if payload.channel_id == 1092355243418861619:
        if str(payload.emoji) == '\N{wrench}':
            fidvazubi = get(payload.member.guild.roles, name='FIDV-Azubi')
            for guild in client.guilds:
                for member in guild.members:
                    for role in member.roles:
                        if role.name == "FIDV" or role.name == "FISI-Azubi" or role.name == "FISI" or role.name == "FIDP-Azubi" or role.name == "FIDP" or role.name == "FIAE-Azubi" or role.name == "FIAE" or role.name == "IT-SE-Azubi" or role.name == "IT-SE" ==True:
                            channel = client.get_channel(1089909009869451277)
                            await channel.send(f" Folgender benutzer hat mehr als 1 Rolle USER_ID: {member.id:d} - USER_NAME: {member.name}  - ROLE: {role.name} - Beigetreten {member.joined_at.strftime('%d.%m.%Y')}")
                            return
                        else:
                            await member.add_roles(fidvazubi)
                            await member.remove_roles(undefined)
        if str(payload.emoji) == '\N{screwdriver}':
            role = get(payload.member.guild.roles, name='FIDV')
            await member.add_roles(role)
            await member.remove_roles(undefined)
        if str(payload.emoji) == '\N{telescope}':
            role = get(payload.member.guild.roles, name='FIDP-Azubi')
            await member.add_roles(role)
            await member.remove_roles(undefined)
        if str(payload.emoji) == '\N{keyboard}':
            role = get(payload.member.guild.roles, name='FIDP')
            await member.add_roles(role)
            await member.remove_roles(undefined)
        if str(payload.emoji) == '\N{ticket}':
            role = get(payload.member.guild.roles, name='FIAE-Azubi')
            await member.add_roles(role)
            await member.remove_roles(undefined)
        if str(payload.emoji) == '\N{Notebook}':
            role = get(payload.member.guild.roles, name='FIAE')
            await member.add_roles(role)
            await member.remove_roles(undefined)
        if str(payload.emoji) == '\N{Personal Computer}':
            role = get(payload.member.guild.roles, name='FISI-Azubi')
            await member.add_roles(role)
            await member.remove_roles(undefined)
        if str(payload.emoji) == '\N{Desktop Computer}':
            role = get(payload.member.guild.roles, name='FISI')
            await member.add_roles(role)
            await member.remove_roles(undefined)
        if str(payload.emoji) == '\N{High Voltage Sign}':
            role = get(payload.member.guild.roles, name='IT-SE-Azubi')
            await member.add_roles(role)
            await member.remove_roles(undefined)
        if str(payload.emoji) == '\N{Electric Plug}':
            role = get(payload.member.guild.roles, name='IT-SE')
            await member.add_roles(role)
            await member.remove_roles(undefined)
        else:
            role = get(guild.roles, name=payload.emoji)

        if role is not None:
            await payload.member.add_roles(role)
            channel = client.get_channel(1089909009869451277)
            await channel.send(
                f"{member.mention} hat die {role.name} Role zugewiesen bekommen")


# Assign the role when the role is added as a reaction to the message.
@client.event
async def on_raw_reaction_remove(payload):
    guild = client.get_guild(payload.guild_id)
    member = get(guild.members, id=payload.user_id)
    undefined = discord.utils.get(member.guild.roles, name="-undefined-")
    if payload.channel_id == 1092355243418861619:
        if str(payload.emoji) == '\N{wrench}':
            role = get(guild.roles, name='FIDV-Azubi')
            await member.remove_roles(role)
            await member.add_roles(undefined)
        if str(payload.emoji) == '\N{screwdriver}':
            role = get(guild.roles, name='FIDV')
            await member.remove_roles(role)
            await member.add_roles(undefined)
        if str(payload.emoji) == '\N{telescope}':
            role = get(guild.roles, name='FIDP-Azubi')
            await member.remove_roles(role)
            await member.add_roles(undefined)
        if str(payload.emoji) == '\N{keyboard}':
            role = get(guild.roles, name='FIDP')
            await member.remove_roles(role)
            await member.add_roles(undefined)
        if str(payload.emoji) == '\N{ticket}':
            role = get(guild.roles, name='FIAE-Azubi')
            await member.remove_roles(role)
            await member.add_roles(undefined)
        if str(payload.emoji) == '\N{Notebook}':
            role = get(guild.roles, name='FIAE')
            await member.remove_roles(role)
            await member.add_roles(undefined)
        if str(payload.emoji) == '\N{Personal Computer}':
            role = get(guild.roles, name='FISI-Azubi')
            await member.remove_roles(role)
            await member.add_roles(undefined)
        if str(payload.emoji) == '\N{Desktop Computer}':
            role = get(guild.roles, name='FISI')
            await member.remove_roles(role)
            await member.add_roles(undefined)
        if str(payload.emoji) == '\N{High Voltage Sign}':
            role = get(guild.roles, name='IT-SE-Azubi')
            await member.remove_roles(role)
            await member.add_roles(undefined)
        if str(payload.emoji) == '\N{Electric Plug}':
            role = get(guild.roles, name='IT-SE')
            await member.remove_roles(role)
            await member.add_roles(undefined)
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji)

        if role is not None:
            await member.remove_roles(role)
            channel = client.get_channel(1089909009869451277)
            await channel.send(
                f"{member.mention} hat die {role.name} Role entfernt bekommen")


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
        channels = client.get_channel(1092355243418861619)
        print('Clearing messages...')
        await channels.purge(limit=1000)
        embed = discord.Embed(title='Wähle die Fachrichtung deines Berufes!',
                              description='nur __eine__ Rolle wählen **!**, bei __Missachtung__ werden alle Rollen entfernt**!**')
        embed.set_author(name="https://www.fachinformatik.it",url="https://www.fachinformatik.it")
        embed.add_field(name='Systemintegeration', value='\N{Desktop Computer}', inline=True)
        embed.add_field(name='Systemintegeration-Azubi', value='\N{Personal Computer}', inline=True)
        embed.add_field(name='Anwendungsentwicklung', value='\N{Notebook}', inline=True)
        embed.add_field(name='Anwendungsentwicklung-Azubi', value='\N{ticket}', inline=True)
        embed.add_field(name='Digitale Vernetzung', value='\N{screwdriver}', inline=True)
        embed.add_field(name='Digitale Vernetzung-Azubi', value='\N{wrench}', inline=True)
        embed.add_field(name='Daten- und Prozessanalyse', value='\N{keyboard}', inline=True)
        embed.add_field(name='Daten- und Prozessanalyse-Azubi', value='\N{telescope}', inline=True)
        embed.add_field(name='IT-Systemelektroniker', value='\N{Electric Plug}', inline=True)
        embed.add_field(name='IT-Systemelektroniker-Azubi', value='\N{High Voltage Sign}', inline=True)
        embed.set_footer(text='Auswahl ist erforderlich, by @Taracraft#0762')
        mess = await channels.send(embed=embed)
        await mess.add_reaction('\N{Desktop Computer}')
        await mess.add_reaction('\N{Personal Computer}')
        await mess.add_reaction('\N{Notebook}')
        await mess.add_reaction('\N{ticket}')
        await mess.add_reaction('\N{screwdriver}')
        await mess.add_reaction('\N{wrench}')
        await mess.add_reaction('\N{keyboard}')
        await mess.add_reaction('\N{telescope}')
        await mess.add_reaction('\N{Electric Plug}')
        await mess.add_reaction('\N{High Voltage Sign}')

if __name__ == '__main__':
    main()

client.run('')
