import os
from dotenv import load_dotenv
import spotipy
import spotipy.oauth2
import playlist


class Recent:
    def __init__(self):
        # Load environ
        load_dotenv()

        # Get id and secret
        self.client_id = os.environ["CLIENT_ID"]
        self.client_secret = os.environ["CLIENT_SECRET"]
        self.redirect_uri = os.environ["REDIRECT_URI"]

        # Arrarys for recent history of tracks, artists
        self.artists = []
        self.tracks = []

        # Names of tracks and artists
        self.names = []

        # limit for tracks
        self.limit = 2
        self.time_range = "short_term"
        self.offset = 0

    def top_tracks(self, sp: spotipy.Spotify):
        tracks = sp.current_user_top_tracks(self.limit, self.offset, self.time_range)

        for track in tracks["items"]:
            self.tracks.append(track["uri"].split(":")[-1])
            self.names.append(track["name"])

    def top_artists(self, sp: spotipy.Spotify):
        artists = sp.current_user_top_artists(self.limit, self.offset, self.time_range)

        for artist in artists["items"]:
            self.artists.append(artist["uri"].split(":")[-1])
            self.names.append(artist["name"])

        


def main():
    recent = Recent()
    spotify = playlist.Playlist()

    sp = spotify.authorize()

    recent.top_tracks(sp)
    recent.top_artists(sp)

    print(recent.tracks)
    print(recent.artists)


if __name__ == "__main__":
    main()
