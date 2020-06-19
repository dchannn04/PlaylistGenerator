import json
import spotipy
import webbrowser
import sys
import spotipy.util as util
import spotipy.oauth2 as oauth2
from json.decoder import JSONDecodeError
import collections
import queue
import random



#-------------------------- Get id for artist ----------------------------------

def get_id_for_artist(artist_name):
    searchResults = spotify.search(artist_name, 1, 0, "artist")
    artist_id = searchResults['artists']['items'][0]['id']
    return artist_id

#-------------------------- Gets related artists for an artist -----------------

def get_related_artists(id, depth):
    child_artists = []
    child_artist_depth = depth + 1
    related_artists = spotify.artist_related_artists(id)
    random.shuffle(related_artists)

    ## get related artists, shuffle and add 5 more artists
    for child_artist in related_artists['artists'][:5]:
        artist_node = artist(child_artist['id'], child_artist['name'],
        child_artist_depth)
        child_artists.append(artist_node)
    return child_artists

#-------------------------- DFS method  ----------------------------------------

def get_artists_for_playlist(artist_id, artist_name, min_depth, max_depth):
    artist_node = artist(artist_id, artist_name, 0)
    frontier = queue.LifoQueue()
    artists = []
    explored = []
    related_artists = []
    artists.append(artist_node.id)
    frontier.put(artist_node)
    while (not frontier.empty()):
        artist_node = frontier.get()

        if (artist_node.id in artists and artist_node.depth < min_depth):
            artists.remove(artist_node.id)

        if (artist_node not in explored):
            if (artist_node.depth >= min_depth and artist_node.id not in artists):
                artists.append(artist_node.id)
            explored.append(artist_node.id)

        if (artist_node.depth != max_depth):
            related_artists=get_related_artists(artist_node.id, artist_node.depth)
            for related_artist in related_artists:
                if (related_artist.id not in explored):
                    frontier.put(related_artist)
    return artists