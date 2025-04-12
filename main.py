import discord
from discord.ext import commands
import os
import json

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "whitelist.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_ready():
    print(f"Bot aktif: {bot.user}")

@bot.command()
async def oyun_ekle(ctx, oyun_id: str):
    data = load_data()
    if oyun_id not in data:
        data.append(oyun_id)
        save_data(data)
        await ctx.send(f"Oyun eklendi: {oyun_id}")
    else:
        await ctx.send("Bu oyun zaten whitelist'te.")

@bot.command()
async def oyun_sil(ctx, oyun_id: str):
    data = load_data()
    if oyun_id in data:
        data.remove(oyun_id)
        save_data(data)
        await ctx.send(f"Oyun silindi: {oyun_id}")
    else:
        await ctx.send("Bu oyun whitelist'te yok.")

@bot.command()
async def oyunlar(ctx):
    data = load_data()
    if data:
        await ctx.send("Whitelist'teki oyunlar:\n" + "\n".join(data))
    else:
        await ctx.send("Whitelist boş.")

bot.run(os.getenv("TOKEN"))