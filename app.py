from flask import Flask, render_template, request
from tweepy import OAuthHandler, API
from client import Client

app = Flask(__name__)

consumer_key = ""
consumer_secret = ""

username = ""
scope = ""
client_id = ""
client_secret = ""
redirect_uri = "http://localhost:8080"

c = Client(username, scope, client_id, client_secret, redirect_uri)
c.auth_spotify(c.token)

auth = OAuthHandler(
    consumer_key, consumer_secret)


@app.route("/")
def main():
    return "welcome bos"


@app.route("/login")
def login():
    data = auth.get_authorization_url()

    return render_template("login.html", data=data)


@app.route("/callback", methods=['GET'])
def callback():
    verifier = request.args.get('oauth_verifier')

    token = auth.get_access_token(verifier)
    access_token = token[0]
    access_secret = token[1]

    new_auth = OAuthHandler(consumer_key, consumer_secret)
    new_auth.set_access_token(access_token, access_secret)
    api = API(new_auth)
    api.update_status(status="Tweeting from Flask")
    return f"Success"


@app.route("/status")
def status():
    return render_template("status.html")


@app.route("/get_info", methods=['GET', 'POST'])
def get_info():
    if request.method == 'GET':
        current_track, current_artist = c.get_track_info()
        cover_art_url = c.get_cover_art_url()

    if request.method == 'POST':
        current_track, current_artist = c.get_track_info()
        cover_art_url = c.get_cover_art_url()
        c.set_is_tweeting()

    data = {"current_track": current_track,
            "current_artist": current_artist,
            "is_tweet": c.is_tweeting,
            "cover_art": cover_art_url}
    return data


if __name__ == "__main__":
    app.run(debug=True)
