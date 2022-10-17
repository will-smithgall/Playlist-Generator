# Playlist Generator

Using the Spotify API and the spotipy python library, this program will generate playlists based off of Spotifys recommendations. These recommendations are generated using the Spotify API with artists, tracks, and genre as seeds for the recommendation algorithm.

## Permissions

By running this program, you will be giving it the ability to read public data, as well as modify public data. The only data that will be modified is the playlist that the program creates, nothing else will be bothered.

## Getting Started

1. Clone the repo
2. Install the requirements 
```sh
pip install -r requirements.txt
```
3. To edit, you will need a to register project in Spotify Developer. this can be done [here](https://developer.spotify.com/dashboard/applications)
4. Create a ```.env``` file. Inside this file you will place your Client ID, Client Secret, as well as the Redirect URI.
```sh
CLIENT_ID="Your client ID"
CLIENT_SECRET="Your client secret"
REDIRECT_URI="Your redirect URI"
```
Note: The redirect URI in this file must be the same as the redirect URI that you put in the dashboard when registering the program

## Usage

After running the program, you will be promted to choose either Automatic or Custom. Custom will allow you to enter your own links, while automatic will generate the playlist based off of your most listened to tracks and artists. Both choices will require a genre to be entered. Respond to said prompt for Spotify's full list of valid genres.