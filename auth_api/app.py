from flask import Flask, jsonify, request, redirect
import requests
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://admin:admin@localhost:27017')
db = client.test
collection = db.users


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
