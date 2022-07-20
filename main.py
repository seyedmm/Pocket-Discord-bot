import discord
from discord import ButtonStyle
from discord.ui import View, Button
import db_connection
import pocket_connection
import json
import os

bot = discord.Bot()
TOKEN = os.getenv("DISCORD_TOKEN")
CONSUMER_KEY = os.getenv("CONSUMER_KEY")


@bot.event
async def on_ready():
    print('Sfg')


@bot.slash_command(name='register')
async def pocket_list(ctx):
    user_dm = await ctx.author.create_dm()
    if not db_connection.is_in_db(ctx.author.id):
        pocket_req_token = pocket_connection.generate_request_token()
        pocket_authorize_url = pocket_connection.generate_authorize_url(pocket_req_token)

        async def done_btn_callback(interaction: discord.Interaction):
            pocket_access_token_query = pocket_connection.generate_access_token(request_token=pocket_req_token)
            try:
                pocket_access_token = json.loads(pocket_access_token_query)['access_token']
            except json.decoder.JSONDecodeError:
                await user_dm.send('Registration failed.\nYou did not grant access to the bot.')
            else:
                db_connection.add_user(ctx.author.id, pocket_access_token)
                await user_dm.send('You have successfully registered')
            finally:
                await interaction.message.delete()

        done_btn = Button(style=ButtonStyle.success, label='Done', emoji=bot.get_emoji(999004472653119619))
        done_btn.callback = done_btn_callback

        view = View()
        view.add_item(done_btn)

        await user_dm.send(
            'Open the link below and click Authorize\n{}\nThen click the Done button below this message'.format(
                pocket_authorize_url), view=view)
        await ctx.respond(f'||<@{ctx.author.id}>||\nCheck your DM')

    else:
        await ctx.respond('You are already registered')


bot.run(TOKEN)
