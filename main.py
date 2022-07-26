from ast import Param
import discord
import discord
from discord import ButtonStyle
from discord.ui import View, Button
import Database
from Pocket import Pocket as PocketClient 
import json
import os
from dotenv import load_dotenv
from Server import app
from GunicornServer import StandaloneApplication
import threading

server = StandaloneApplication(app,{"bind":f"0.0.0.0:{os.getenv('PORT')}"})

Pocket = PocketClient()


load_dotenv()
bot = discord.Bot()
TOKEN = os.getenv("DISCORD_TOKEN")
t = threading.Thread(target=bot.run, args=(TOKEN,))

@bot.event
async def on_ready():
    print(f'Bot started.\n{bot.user.name}\n{bot.user.id}\n------------------------')


@discord.guild_only()
@bot.slash_command(name='register')
async def pocket_list(ctx):
    user_dm = await ctx.author.create_dm()
    if not Database.is_in_db(ctx.author.id):
        redirect_uri = f'{os.getenv("MAIN_URL")}/authentication/{ctx.author.id}'
        pocket_req_token = Pocket.get_request_token(redirect_uri)
        pocket_authorize_url = Pocket.generate_authorize_url(pocket_req_token,redirect_uri)
        await user_dm.send(
            'Open the link below and click Authorize\n{}\nThen click the Done button below this message'.format(
                pocket_authorize_url))

    else:
        await ctx.respond('You are already registered')
t.start()
app.run()


