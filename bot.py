import os
import random
import discord

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # enable in Discord Dev Portal too
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    text = message.content.lower().strip()

    # Case A: exact phrase
    if text == "@grok is this real":
        await message.channel.send(random.choice(["Yes", "No"]))
        return

    # Case B: user actually mentions the bot and asks "is this real"
    if client.user in message.mentions and "is this real" in text:
        await message.channel.send(random.choice(["Yes", "No"]))
        return

client.run(TOKEN)
