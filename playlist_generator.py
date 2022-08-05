from playlist import Playlist
from recommendations import Recommendations
import os
import time


def main():
    print("This program will require authentication to access and create spotify playlists.\nYou will be redirected to a login page, and redirected again from there.\nOnce redirected, copy that link and follow the instructions.")
    time.sleep(10)

    # Define playlist and rec objects
    playlist = Playlist()
    recommendations = Recommendations()

    # Authorize user
    sp = playlist.authorize()
    token = recommendations.get_token()

    user = playlist.get_user(sp)
    temp_name = "test"
    description = "beep boop"

    new_playlist = playlist.init_playlist(sp, user, temp_name, description)
    playlist_id = new_playlist["id"]

    # Get user input for artists, genres, tracks, and the size of playlist
    count = 0
    artists = []
    tracks = []
    genre = []
    valid_genres = recommendations.get_valid_genres()

    # Clear the terminal, make it cleaner
    os.system("clear")

    while count < 2:
        artists.append(input(f"Enter the URL for an artist ({count + 1}/2): "))
        count += 1

    count = 0
    while count < 2:
        tracks.append(input(f"Enter the URL for a track ({count + 1}/2): "))
        count += 1

    flag = True
    while flag:
        temp = input("Enter one genre for the generator (lowercase). Type ? to see all valid genres: ")
        if temp in valid_genres:
            genre.append(temp)
            flag = False
        elif temp == "?":
            for g in valid_genres:
                print(f"*{g}")
        else:
            print("That genre was not recognized, please enter a new one.")

    amount = input("Enter the size of the playlist: ")
    recommendations.set_seeds(artists, genre, tracks)

    success = recommendations.recommendations(token, amount)

    if success == -1:
        playlist.delete_playlist(sp, playlist_id)
        quit()

    track_recs = recommendations.get_recommendations()

    name = input("Enter a name for the playlist: ")

    # Take generated recommendations and add to the generated playlist
    playlist.set_name(sp, playlist_id, name, description)
    playlist.add_track(sp, track_recs, playlist_id)

    print(f"Playlist with name {name} created with {amount} tracks.")

if __name__ == "__main__":
    main()
