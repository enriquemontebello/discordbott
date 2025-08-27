import os
import random
import asyncio
import discord
from aiohttp import web

TOKEN = os.getenv("DISCORD_TOKEN")
PORT = int(os.getenv("PORT", "10000"))  # Render provides PORT

# ---- Tiny keepalive HTTP server for Render ----
async def handle_root(request):
    return web.Response(text="ok")

async def start_web():
    app = web.Application()
    app.add_routes([web.get("/", handle_root)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

# ---- Discord bot ----
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    text = message.content.lower().strip()

    # Exact phrase
    if text == "@grok is this real":
        await message.channel.send(random.choice(["Yes", "No"]))
        return

    # Mention + phrase (optional)
    if client.user in message.mentions and "is this real" in text:
        await message.channel.send(random.choice(["Yes", "No"]))
        return

async def main():
    # run both the web server and the bot together
    await start_web()
    await client.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
