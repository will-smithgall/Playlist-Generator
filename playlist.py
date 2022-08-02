import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class Playlist:
    def __init__(self):

        # Load environmental variables
        load_dotenv()

        # Define environ variables
        self.client_id = os.environ["CLIENT_ID"]
        self.client_secret = os.environ["CLIENT_SECRET"]
        self.redirect_uri = os.environ["REDIRECT_URI"]

        # Define scopes
        self.scope = "playlist-modify-public"

    def authorize(self):

        # Pass environ variables to spotipy to complete OAuth
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=self.scope,
                show_dialog=True,
            )
        )

        # Return Spotify object
        return sp

    def get_user(self, sp: spotipy.Spotify):

        # Return user ID of current registered user
        return sp.me()["id"]

    def id(self):

        return self.playlist_id

    def set_playlist_id(self, playlist_id):

        self.playlist_id = playlist_id

    def init_playlist(self, sp: spotipy.Spotify, user, name, description):

        # Initialize Spotify playlist from instance variables
        playlist = sp.user_playlist_create(user, name, True, False, description)
        return playlist

    def add_track(self, sp: spotipy.Spotify, track_uris, playlist_id):

        # Add track(s) to specified playlist
        sp.playlist_add_items(playlist_id, track_uris, 0)


def main():
    playlist = Playlist()

    sp = playlist.authorize()

    user = playlist.get_user(sp)
    name = "test"
    description = "beep boop"

    plist = playlist.init_playlist(sp, user, name, description)
    playlist_id = plist["id"]

    uri = ["spotify:track:2Djdr6SndwgHqOXHVeJmCu"]
    playlist.add_track(sp, uri, playlist_id)


if __name__ == "__main__":
    main()
