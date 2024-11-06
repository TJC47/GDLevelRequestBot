import requests
import time
import json
import random
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from threading import Thread
import hashlib
import base64
"""
--- CONFIGURATION SECTION ---
This is the user config section. Please adjust these to your needs.
"""

# CHANNELS
REQUEST_CHANNELID = 1188171217241391126
REQUESTLOG_CHANNELID = 1302012133344542740
BOT_USERID = 1300431457390563328

"""
--- CONFIGURATION SECTION END ---
"""
f = open("token.txt")
TOKEN = f.readline()
f.close()
requestslist = []

class MyClient(discord.Client):
    global requestslist
    """Copy pasted from random github repo"""
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
        await self.tree.sync()
    async def on_message(self, message):
        global requestslist
        if message.content.startswith("y!help"):
            await message.channel.send("""## Help
-# ***please note that these are not the slash commands. for a list of the slash commands use discord's UI***
-# **y!help** - Displays this message. Do you really need help for the help?
-# **y!useless** - Useless command. Don't use.
-# **y!request** - Request a Geometry Dash level.
-# **y!getrequest** - Chooses a random ID for requests
-# **y!q** - shows the entire level request queue
-# **y!rlog** - shows level request logs""")
            await message.add_reaction("✅")
        elif message.content == f"<@{str(BOT_USERID)}>":
            await message.channel.send("Yo mate, if ya need help, use da y!help command. Thanks and bye.")
        elif message.content.startswith("y!useless"):
            await message.channel.send(f"This command is absolutely useless. Why did you use it?\n# AND I TOLD YOU NOT TO USE IT")
            await message.add_reaction("✅")
        elif message.content.startswith("y!request"):
            levelid = message.content.split(" ", 1)[1]
            requestchannel = client.get_channel(REQUEST_CHANNELID)
            requestmessage = await requestchannel.send(f"{levelid} - requested by {message.author.mention}({message.author.name})")
            requestslist.append(f"{levelid} - requested by {message.author.mention}({message.author.name})")
            await message.add_reaction("✅")
            await message.delete()
            requestlogchannel = client.get_channel(REQUESTLOG_CHANNELID)
            await requestlogchannel.send(f"```[ADD] {levelid} - requested by {message.author.mention}({message.author.name})```")
            f = open("lvlrequestlog.txt", "a")
            f.write("\n" + f"[ADD] {levelid} - requested by {message.author.mention}({message.author.name})")
            f.close()
            f = open("requestmessageids.txt", "a")
            f.write("\n" + str(requestmessage.id))
            f.close()
            await requestmessage.add_reaction("✅")
        elif message.content.startswith("y!getrequest"):
            try:
                request = random.choice(requestslist)
                requestslist.remove(request)
                await message.channel.send(f"Random Level ID:\n-# {request}")
                await message.add_reaction("✅")
                requestlogchannel = client.get_channel(REQUESTLOG_CHANNELID)
                await requestlogchannel.send(f"```[GET] {request} - {message.author.mention}({message.author.name})```")
                f = open("lvlrequestlog.txt", "a")
                f.write("\n" + f"[GET] {request} - {message.author.mention}({message.author.name})")
                f.close()
            except:
                await message.channel.send(f"Random Level ID:\n-# The queue is empty!")
                await message.add_reaction("❌")
        elif message.content.startswith("y!rlog"):
            try:
                f = open("lvlrequestlog.txt", "r")
                output = f.read()
                f.close()
                await message.channel.send(f"Request log:\n```{output}```")
                await message.add_reaction("✅")
            except:
                await message.channel.send(f"Request log:\n-# Something error happened")
                await message.add_reaction("❌")
        elif message.content.startswith("y!rpurge"):
            try:
                f = open("requestmessageids.txt", "r")
                messageids = f.read()
                f.close()
                messageids = messageids.split("\n")
                requestchannel = client.get_channel(REQUEST_CHANNELID)
                for messageid in messageids:
                    try:
                        if messageid == "" or messageid == "\n":
                            pass
                        else:
                            requestmessage = await requestchannel.fetch_message(int(messageid))
                            await requestmessage.delete()
                    except:
                        pass
                f = open("requestmessageids.txt", "w")
                f.write("")
                f.close()
                requestslist = []
                requestlogchannel = client.get_channel(REQUESTLOG_CHANNELID)
                await requestlogchannel.send(f"```[PURGE] Initiated by {message.author.mention}({message.author.name})```")
                f = open("lvlrequestlog.txt", "a")
                f.write("\n" + f"[PURGE] Initiated by {message.author.mention}({message.author.name})")
                f.close()
                await message.add_reaction("✅")
                await message.delete()
            except:
                await message.add_reaction("❌")
                await message.delete()
        elif message.content.startswith("y!q"):
            try:
                if len(requestslist) == 0:
                    await message.channel.send(f"Level request queue:\n-# The queue is empty!")
                    await message.add_reaction("❌")
                else:
                    output = ""
                    for request in requestslist:
                        output = output + "\n-# " + request
                    await message.channel.send(f"Level request queue:{output}")
                    await message.add_reaction("✅")
            except:
                await message.channel.send(f"Level request queue:\n-# The queue is empty!")
                await message.add_reaction("❌")
        elif "(╯°□°)╯︵ ┻━┻" in message.content:
            await message.channel.send("┬─┬ノ(ಠ_ಠノ)")
        else:
            if message.content.startswith("y!"):
                await message.channel.send(f"This command doesn't seem to exist. **Yet**. Type y!help to get a list of the commands you can use.")
                await message.add_reaction("❌")
intents = discord.Intents.all()
client = MyClient(intents=intents)

@client.tree.command(description="Sends a message")
@app_commands.describe(
    message='content of message'
)
@app_commands.allowed_installs(guilds=True, users=True)
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(content=f"{message}")

@client.tree.command(description="Request a level")
@app_commands.describe(
    levelid='id of the level'
)
@app_commands.allowed_installs(guilds=True, users=True)
async def request(interaction: discord.Interaction, levelid: int):
            await interaction.response.defer(ephemeral=True)
            levelid = str(levelid)
            requestchannel = client.get_channel(REQUEST_CHANNELID)
            requestmessage = await requestchannel.send(f"{levelid} - requested by {interaction.user.mention}({interaction.user.name})")
            requestslist.append(f"{levelid} - requested by {interaction.user.mention}({interaction.user.name})")
            requestlogchannel = client.get_channel(REQUESTLOG_CHANNELID)
            await requestlogchannel.send(f"```[ADD] {levelid} - requested by {interaction.user.mention}({interaction.user.name})```")
            f = open("lvlrequestlog.txt", "a")
            f.write("\n" + f"[ADD] {levelid} - requested by {interaction.user.mention}({interaction.user.name})")
            f.close()
            f = open("requestmessageids.txt", "a")
            f.write("\n" + str(requestmessage.id))
            f.close()
            await requestmessage.add_reaction("✅")
            await interaction.followup.send(content="Your request has been carefully noted.")


@client.tree.command(description="Delete all requests in the request channel")
@app_commands.allowed_installs(guilds=True, users=True)
async def rpurge(interaction: discord.Interaction):
    try:
        await interaction.response.defer(ephemeral=True)
        f = open("requestmessageids.txt", "r")
        messageids = f.read()
        f.close()
        messageids = messageids.split("\n")
        requestchannel = client.get_channel(REQUEST_CHANNELID)
        for messageid in messageids:
            try:
                if messageid == "" or messageid == "\n":
                    pass
                else:
                    requestmessage = await requestchannel.fetch_message(int(messageid))
                    await requestmessage.delete()
            except:
                pass
        f = open("requestmessageids.txt", "w")
        f.write("")
        f.close()
        requestslist = []
        requestlogchannel = client.get_channel(REQUESTLOG_CHANNELID)
        await requestlogchannel.send(f"```[PURGE] Initiated by {interaction.user.mention}({interaction.user.name})```")
        f = open("lvlrequestlog.txt", "a")
        f.write("\n" + f"[PURGE] Initiated by {interaction.user.mention}({interaction.user.name})")
        f.close()
        await interaction.followup.send(content="Deleted requests successfully")
    except:
        await interaction.followup.send(content="Deletion was error")

@client.tree.command(description="Useless command. Do not use.")
@app_commands.allowed_installs(guilds=True, users=True)
async def useless(interaction: discord.Interaction):
    await interaction.response.send_message(content=f"This command is absolutely useless. Why did you use it?\n# AND I TOLD YOU NOT TO USE IT")

@client.tree.command(description="Get help for non-slash commands")
@app_commands.allowed_installs(guilds=True, users=True)
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(content=f"""## Help
-# ***please note that these are not the slash commands. for a list of the slash commands use discord's UI***
-# **y!help** - Displays this message. Do you really need help for the help?
-# **y!useless** - Useless command. Don't use.
-# **y!request** - Request a Geometry Dash level.
-# **y!getrequest** - Chooses a random ID for requests
-# **y!q** - shows the entire level request queue
-# **y!rlog** - shows level request logs""")

client.run(TOKEN)
