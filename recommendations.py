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

    # Returns 1 if it successfully gets recommendations, returns -1 if an error is encountered.
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
        try:
            for element in response["tracks"]:
                self.recommended_uris.append(element["uri"])

            return 1
        except KeyError as e:
            print(
                "\nThere was an error getting the recommendations.\nThis is usually due to an invalid URL being passed.\nPlease check your artist and track URLs and try again!"
            )
            return -1

    def get_recommendations(self):
        return self.recommended_uris

    def set_seeds(self, artists, genres, tracks):
        # Get artist id from URL
        for artist in artists:
            link = artist.split("/")[-1]

            if "?" in link:
                link = link.split("?")
                self.artists.append(link[0])
            else:
                self.artists.append(link)

        # Get track id from URL
        for track in tracks:
            link = track.split("/")[-1]

            if "?" in link:
                link = link.split("?")
                self.tracks.append(link[0])
            else:
                self.tracks.append(link)

        # Add genres
        self.genres = genres


def main():
    recs = Recommendations()

    token = recs.get_token()

    # These will be passed in by the user, temp for now
    artists = [
        "https://open.spotify.com/artist/7nCgNmfYJcsVy3vOOzExYS?si=X-C3ldlTRtiRyZtSKqfcGg",
        "https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02",
    ]
    genres = "jazz,funk"
    tracks = [
        "https://open.spotify.com/track/1UvaZaHkh3D9AkmBrrnbFg",
        "https://open.spotify.com/track/0ECGnyHCiGOzEkXY1c5yJ2",
    ]

    # recs.recommendations(token, 10, artists, genres, tracks)
    # print(recs.get_recommendations())

    recs.set_seeds(artists, genres, tracks)
    print(recs.artists)
    print(recs.tracks)


if __name__ == "__main__":
    main()
