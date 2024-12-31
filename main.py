from dotenv import load_dotenv
import discord
import os
from upstash_redis import Redis
from datetime import datetime

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
redis = Redis.from_env()

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

discord_token = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hey!")

@bot.event
async def on_message(message):
    
    if message.author == bot.user:
        return

    current_time = datetime.now().isoformat() 

    redis.lpush("messages", {
        "id": message.id,
        "message": message.content,
        "author_id": message.author.id,
        "channel_id": message.channel.id,
        "timestamp_iso": current_time
    })

    await message.channel.send("Message registered in Redis")

bot.run(token)

