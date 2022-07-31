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

import asyncio

load_dotenv()
bot = discord.Bot()
TOKEN = os.getenv("DISCORD_TOKEN")
t = threading.Thread(target=bot.run, args=(TOKEN,))

@bot.event
async def on_ready():
    print(f'Bot started.\n{bot.user.name}\n{bot.user.id}\n------------------------')


@discord.guild_only()
@bot.slash_command(name='register')
async def register(ctx):
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

def embed_generator(item_id: str, title: str, url: str, is_favorite: bool):
    embed = discord.Embed(title=title, url=url)
    embed.add_field(name=':page_facing_up: Title:', value=title, inline=False)
    embed.add_field(name=':keyboard: Url:', value=url, inline=False)
    embed.add_field(name=':heart: Favorite:', value='<:star_fillpng:1001008928248836128>Yes' if is_favorite else '<:star_notfillpng:1001008899987615755>No', inline=False)
    embed.add_field(name=':id: Unique ID:', value=item_id, inline=False)
    return embed


@bot.slash_command(name='list')
async def pocket_list(ctx,
               state: discord.Option(choices=['unread', 'archive', 'all']),
               favorite: bool = None,
               max_count: int = 15, ):
    if not Database.is_in_db(ctx.author.id):
        await ctx.respond("Please /register first.")
        return
    token = Database.get_user(ctx.author.id).access_token
    pocket_item_list = Pocket.get_pocket_list(token, count=max_count, favorite=(1 if favorite == True else 0), state=state)
    embed_list = list()
    embed_index = 1
    for pocket_item in pocket_item_list:
        embed = embed_generator(
            item_id=pocket_item['item_id'],
            title=pocket_item['given_title'],
            url=pocket_item['given_url'],
            is_favorite=True if pocket_item['favorite'] == '1' else False)
        embed.set_footer(text=f'Page {embed_index} of {len(pocket_item_list)}')
        embed_index += 1
        embed_list.append(embed)
    pages = len(embed_list)
    cur_page = 1

    await ctx.respond('Your Pocket list:')
    message = await ctx.send(embed=embed_list[cur_page - 1])
    # getting the message object for editing and reacting

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this

            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                await message.edit(embed=embed_list[cur_page - 1])
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                await message.edit(embed=embed_list[cur_page - 1])
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
        except asyncio.TimeoutError:
            await message.clear_reactions()
            break
            # ending the loop if user doesn't react after x seconds

t.start()
app.run()


