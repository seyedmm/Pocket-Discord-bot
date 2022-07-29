from flask import Flask, request, abort
from flask.templating import render_template
from Pocket import Pocket as PocketClient
from Database import add_user
from discord import Embed
import asyncio
app = Flask(__name__,
            static_folder='web/static',
            template_folder='web/templates')

pending_authentication = {}
loop = asyncio.get_event_loop()

Pocket = PocketClient()

def show_pends():
    print(pending_authentication)


@app.route("/authentication", methods=['GET'])
def auth():
    uid = request.args.get('uid')
    if not uid:
        abort(400)
    elif not pending_authentication.get(uid):
        abort(404)
    request_code = pending_authentication[uid][0]
    ctx_object = pending_authentication[uid][1]
    del pending_authentication[uid]
    final_request = Pocket.get_access_token(request_code)
    if final_request.status_code == 403:
        return render_template('auth.html', {"title": "You have rejected to give the required permissions to the bot.", "message": "It can't function without these permissions. Please return back to discord and click again on the link"})
    
    add_user(uid, final_request.json()['access_token'], pocket_username=final_request.json()['username'])
    user_dm = ctx_object.author.dm_channel
    embed = Embed(title="Authentication successful",
                  description="The bot has been successfully authenticated. You can now use it.", color=0x00FF00)
    loop.run_until_complete(user_dm.send(embed=embed))
    return render_template('auth.html', {'title': "Successfully authenticated", 'message':'The bot has been successfully authenticated. You can now use it.'})


@ app.route("/")
def rickroll():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
