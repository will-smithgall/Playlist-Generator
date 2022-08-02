import base64
import os
from dotenv import load_dotenv
import json
import requests


class Recommendations:
    def __init__(self):
        # Load in environment variables
        load_dotenv()

        # Array of recommended song URIs
        self.recommended_uris = []

        # Get id and secret as environ variables
        self.client_id = os.environ["CLIENT_ID"]
        self.client_secret = os.environ["CLIENT_SECRET"]

        # List of valid genres
        self.valid_genres = []

        # Empty seed values
        self.artists = []
        self.tracks = []
        self.genres = []

    def get_token(self):
        token_url = "https://accounts.spotify.com/api/token"

        # Token request
        response = requests.post(
            token_url,
            headers={
                "Authorization": "Basic "
                + base64.b64encode(
                    f"{self.client_id}:{self.client_secret}".encode("ascii")
                ).decode("ascii"),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            params={"grant_type": "client_credentials"},
        )

        # Return JSON of API response
        return response.json()

    def get_valid_genres(self):
        with open("Files/valid_genres.json") as f:
            data = json.load(f)

            for entry in data["genres"]:
                self.valid_genres.append(entry)

        return self.valid_genres

    def recommendations(self, token, amount):
        rec_url = "https://api.spotify.com/v1/recommendations"

        # Requests call for Spotify recommended tracks

        r = requests.get(
            rec_url,
            headers={
                "Authorization": f"Bearer {token['access_token']}",
                "Content-Type": "application/json",
            },
            params={
                "seed_artists": ",".join(self.artists),
                "seed_generes": ",".join(self.genres),
                "seed_tracks": ",".join(self.tracks),
                "limit": amount,
            },
        )

        response = r.json()

        # Get URI for each track in response
        for element in response["tracks"]:
            self.recommended_uris.append(element["uri"])

    def get_recommendations(self):
        return self.recommended_uris

    def set_seeds(self, artists, genres, tracks):
        # Get artist id from URL
        for artist in artists:
            link = artist.split("/")
            self.artists.append(link[-1])

        # Get track id from URL
        for track in tracks:
            link = track.split("/")[-1].split("?")
            self.tracks.append(link[0])

        # Add genres
        self.genres = genres


def main():
    recs = Recommendations()

    token = recs.get_token()

    # These will be passed in by the user, temp for now
    artists = [
        "https://open.spotify.com/artist/7ENzCHnmJUr20nUjoZ0zZ1",
        "https://open.spotify.com/artist/4UpA1KitN1RgIZVyWDbZ0U",
    ]
    genres = "jazz,funk"
    tracks = [
        "https://open.spotify.com/track/2NZUXUA8gGmXXw5MayF63k?si=496b37bbfdd14fa8",
        "https://open.spotify.com/track/1HJXdfuWc6IlKBMLtITaHD?si=ebdb690f2db9490c",
    ]

    # recs.recommendations(token, 10, artists, genres, tracks)
    # print(recs.get_recommendations())

    recs.set_seeds(artists, genres, tracks)
    print(recs.tracks)


if __name__ == "__main__":
    main()
