import logging

import spotipy
import spotipy.util

import spotify_secrets

log = logging

sp = None
device_id = None

DEVICE_NAME = 'OD-11'


def init_spotipy():
    token = spotipy.util.prompt_for_user_token(
        spotify_secrets.USERNAME,
        spotify_secrets.SCOPE,
        client_id=spotify_secrets.CLIENT_ID,
        client_secret=spotify_secrets.CLIENT_SECRET,
        redirect_uri=spotify_secrets.REDIRECT_URI)

    global sp
    sp = spotipy.Spotify(auth=token)

    devices = [v['id'] for v in sp.devices()['devices']
               if v['name'] == DEVICE_NAME]
    if not devices:
        raise Exception('OD-11 spotify device not found')
    global device_id
    device_id = devices[0]


def find_spotify_track(artist, title):
    if sp is None:
        init_spotipy()

    title = title.replace('\'', '')

    query = 'artist:"%s" track:"%s"' % (artist, title)
    results = sp.search(q=query, limit=1)

    if not results['tracks']['items']:
        query = 'artist:"%s" %s' % (artist, title)
        results = sp.search(q=query, limit=1)

    if not results['tracks']['items']:
        query = artist + ' ' + title
        results = sp.search(q=query, limit=1)

    if not results['tracks']['items']:
        return (None, None, None)

    item = results['tracks']['items'][0]
    return (item['artists'][0]['name'], item['name'], item['uri'])


def play_spotify_track(uri):
    sp.start_playback(device_id, uris=[uri])
