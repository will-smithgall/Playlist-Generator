from playlist import Playlist
from recommendations import Recommendations


def main():

    # Define playlist and rec objects
    playlist = Playlist()
    recommendations = Recommendations()

    # Generate recommendations based on set inputs (get inputs from user later on)
    token = recommendations.get_token()

    # Get user input for artists, genres, tracks, and the size of playlist
    count = 0
    artists = []
    tracks = []
    genre = []
    valid_genres = recommendations.get_valid_genres()

    while count < 2:
        artists.append(input(f"Enter the URL for an artist ({count + 1}/2): "))
        count += 1

    count = 0
    while count < 2:
        tracks.append(input(f"Enter the URL for a track ({count + 1}/2): "))
        count += 1

    flag = True
    while flag:
        temp = input("Enter one genre for the generator. Type ? to see all valid genres: ")
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

    recommendations.recommendations(token, amount)
    track_recs = recommendations.get_recommendations()

    # Take generated recommendations and add to a new playlist
    sp = playlist.authorize()

    user = playlist.get_user(sp)
    name = "test" #name = input("Enter a name for the playlist: ")
    description = "beep boop"

    new_playlist = playlist.init_playlist(sp, user, name, description)
    playlist_id = new_playlist["id"]

    playlist.add_track(sp, track_recs, playlist_id)

    print(f"Playlist with name {name} created with {amount} tracks.")


if __name__ == "__main__":
    main()
