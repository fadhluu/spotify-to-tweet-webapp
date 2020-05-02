import spotipy
import spotipy.util as util
import requests
import io
from PIL import Image


class Client(object):
    def __init__(self, username, scope, client_id, client_secret, redirect_uri):
        # self.token = util.prompt_for_user_token(
        #     username=username, scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
        self.token = spotipy.SpotifyOAuth(
            username=username, scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
        self.sp = self.auth_spotify(self.token)
        self.is_tweeting = True
        self.cover_art_path = "static/cover_art.png"

    def auth_spotify(self, token):
        sp = spotipy.Spotify(token)
        return sp

    def currently_playing(self):
        return self.sp.currently_playing()

    def set_is_tweeting(self):
        self.is_tweeting = not self.is_tweeting

    def get_track_info(self):
        current_playback = self.currently_playing()
        track_name = current_playback["item"]["name"]
        artist = current_playback["item"]["artists"][0]["name"]

        return track_name, artist

    def get_cover_art(self):
        current_playback = self.currently_playing()
        re = requests.get(
            current_playback["item"]["album"]["images"][0]["url"])

        media = Image.open(io.BytesIO(re.content))
        media.save(self.cover_art_path)

    def get_cover_art_url(self):
        current_playback = self.currently_playing()
        return current_playback["item"]["album"]["images"][0]["url"]
