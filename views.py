from django.shortcuts import render
import discord
from discord.ext import commands
import asyncio

# Define the intents your bot needs
intents = discord.Intents.default()
intents.typing = False
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def hi(ctx):
    await ctx.send('Hello, world!')

bot.run('MTE1Mzk2OTAzNjY4MjYxMjg3OQ.GlCUPq.lnKZM9bNZHOlJv4zbnRazneZ4qdOWXEC9kOt5s')


# Create your views here.
