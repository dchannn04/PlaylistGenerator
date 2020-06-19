import collections
import random
import webbrowser
import spotipy
from spotipy import util
from plistgenerator import get_id_for_artist, get_artists_for_playlist


def generate(acc_name, playlist_name, artist_name):

    client_id = "--------------------"
    client_secret = "--------------------"
    redirect_uri = "bpm-gen-login://callback"



   # acc_name = input('Enter your Spotify account name: ')

   # playlist_name = input('Playlist Name: ')

   # artist_name = input('Artist: ')

    print('Creating Playlist...', playlist_name, )



    artist = collections.namedtuple('artist', 'id name depth')

    token = util.prompt_for_user_token(acc_name, "playlist-modify-public",

                                       client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)



    if token:

        spotify = spotipy.Spotify(auth=token)

        spotify.trace = False

        print("Generating playlist...")

        tmp_artist_id = get_id_for_artist(artist_name)



        # DFS to obtain related artists

        artists = get_artists_for_playlist(tmp_artist_id, artist_name, 2, 5)

        track_ids = []

        for artist in artists:

            results = spotify.artist_top_tracks(artist)  ##ID

            random.shuffle(results)



            ## shuffle the artists songs, pick one

            for track in results['tracks'][:3]:

                tmp_track = "spotify:track:" + track['id']

                track_ids.append(tmp_track)

        random.shuffle(track_ids)



        ## create the playlist

        playlists = spotify.user_playlist_create(acc_name, playlist_name)

        webbrowser.open(playlists['external_urls']['spotify'])



        ## add the tracks to playlisst

        spotify.user_playlist_add_tracks(acc_name, playlists['id'], track_ids)

        print("Success")
