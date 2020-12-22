from flask import Flask, jsonify, request, redirect, url_for
import requests
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient('mongodb://admin:admin@localhost:27017')
db = client.test
collection = db.users

secret = ""



@app.route('/twitter')
def get_verifier():
    oauth_token_tmp = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    res = requests.post(
        'https://api.twitter.com/oauth/access_token?oauth_token=' + oauth_token_tmp + '&oauth_verifier=' + oauth_verifier)
    res_split = res.text.split('&')
    oauth_token = res_split[0].split('=')[1]
    oauth_secret = res_split[1].split('=')[1]
    userid = res_split[2].split('=')[1]
    username = res_split[3].split('=')[1]
    doc = collection.find_one_and_update(
        {
            "data.twitter.oauth_token": oauth_token_tmp
        },
        {
            "$set":
                {
                    "data.twitter.oauth_token": oauth_token,
                    "data.twitter.oauth_token_secret": oauth_secret,
                    "data.twitter.last_seen_id": "1",
                    "data.twitter.user_id": userid,
                    "data.twitter.screen_name": username
                }
        })

    return redirect('http://t.me/TwiVk_bot')


@app.route('/vk')
def get_verifier_vk():
    print(request.args)
    code = request.args.get('code')
    chat_id = request.args.get('state')
    callback_uri = url_for('get_verifier_vk', _external=True)
    link = f"https://oauth.vk.com/access_token?client_id=7705522&client_secret={secret}&redirect_uri={callback_uri}&code={code}"
    res = requests.post(link)
    res_json = res.json()
    access_token = res_json["access_token"]
    print(access_token)
    doc = collection.find_one_and_update(
        {
            "chat_id": chat_id
        },
        {
            "$set":
                {
                    "data.vk.oauth_token": access_token
                }
        })

    return redirect('http://t.me/TwiVk_bot')


@app.route("/auth_vk")
def get_auth_vk():
    ...


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
