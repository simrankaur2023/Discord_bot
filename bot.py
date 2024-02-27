
import discord
from discord.ext import commands
import sqlite3
import asyncio
import datetime

intents = discord.Intents.default()
intents.typing = False
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)


def drop_table_if_exists():
    conn = sqlite3.connect('standup_responses.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS standup_responses')
    conn.commit()
    conn.close()


def init_database():
    conn = sqlite3.connect('standup_responses.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS standup_responses (
        user_id INTEGER PRIMARY KEY,
        date DATE,
        today_plan TEXT,
        yesterday_done TEXT,
        blockers TEXT
    )
    ''')
    conn.commit()
    conn.close()


async def ask_question(ctx, question):
    await ctx.send(question)

    def check(response):
        return response.author == ctx.author and response.channel == ctx.channel

    try:
        user_response = await bot.wait_for("message", check=check, timeout=180)
        return user_response.content
    except asyncio.TimeoutError:
        await ctx.send("You didn't provide a response in time.")
        return None


@bot.command()
async def standup(ctx):
    drop_table_if_exists()  # Remove the existing table if it exists
    init_database()
    user_id = ctx.author.id
    today_date = datetime.datetime.now()

    today_plan = await ask_question(ctx, "1. What will you do today?")
    if today_plan is None:
        return

    yesterday_done = await ask_question(ctx, "2. What did you do yesterday?")
    if yesterday_done is None:
        return

    blockers = await ask_question(ctx, "3. Any blockers?")
    if blockers is None:
        return

    conn = sqlite3.connect('standup_responses.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM standup_responses WHERE user_id = ? AND date = ?', (user_id, today_date))
    existing_entry = cursor.fetchone()

    if existing_entry:
        cursor.execute('''
        UPDATE standup_responses 
        SET today_plan = ?, yesterday_done = ?, blockers = ? 
        WHERE user_id = ? AND date = ?
        ''', (today_plan, yesterday_done, blockers, user_id, today_date))
    else:
        cursor.execute('''
        INSERT INTO standup_responses (user_id, date, today_plan, yesterday_done, blockers)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, today_date, today_plan, yesterday_done, blockers))

    conn.commit()
    conn.close()

    await ctx.send("Thank you for your standup update! It has been recorded.")

bot.run('bot token')



