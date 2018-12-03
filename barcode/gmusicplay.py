import time
import argparse
import requests
import tempfile
import subprocess

from gmusicapi import Mobileclient

import gmusic_secrets

api = None
track_id_info_lookup = None


def init_gmusic_api():
    t0 = time.time()
    print('init_gmusic_api')
    global api
    api = Mobileclient()
    logged_in = api.login(gmusic_secrets.USERNAME, gmusic_secrets.PW, Mobileclient.FROM_MAC_ADDRESS)
    assert(logged_in)
    print('init_gmusic_api finished: %0.2f' % (time.time() - t0))


def init_gmusic_track_id_info():
    global track_id_info_lookup
    lib = api.get_all_songs()
    thumbs_up = [t for t in lib if t.get('rating') == '5']
    track_id_info_lookup = {
        t['id']: (t['artist'], t['title']) for t in thumbs_up}


def play_mp3_file_blocking(f):
    print('play_mp3_file_blocking')
    subprocess.call(['mpg321', '-q', '-a', 'bluealsa', f.name])


def stream_mp3_url_blocking(url):
    print('stream_mp3_url_blocking')
    subprocess.call(['mplayer', '-cache', '20000', '-msgmodule', '-msglevel', 'global=0:statusline=-1',
                     '-ao', 'alsa:device=bluealsa', url])


def play_gmusic_track_blocking(track_id, verbose=False):
    if api is None:
        init_gmusic_api()

    t0 = time.time()
    print('play_gmusic_track_blocking')
    track_url = api.get_stream_url(track_id, device_id=gmusic_secrets.DEVICE_ID)
    print('play_gmusic_track_blocking got url: %0.2f' % (time.time() - t0))

    if verbose:
        print(track_url)

    resp = requests.get(track_url)
    resp.raise_for_status()

    with tempfile.NamedTemporaryFile('wb') as f:
        f.write(resp.content)
        print('play_gmusic_track_blocking got content: %0.2f' % (time.time() - t0))
        play_mp3_file_blocking(f)


def stream_gmusic_track_blocking(track_id, verbose=False):
    if api is None:
        init_gmusic_api()

    t0 = time.time()
    print('play_gmusic_track_blocking')
    track_url = api.get_stream_url(track_id, device_id=gmusic_secrets.DEVICE_ID)
    print('play_gmusic_track_blocking got url: %0.2f' % (time.time() - t0))

    if verbose:
        print(track_url)

    stream_mp3_url_blocking(track_url)


def get_gmusic_track_info(track_id):
    if api is None:
        init_gmusic_api()

    global track_id_info_lookup
    if track_id_info_lookup is None:
        init_gmusic_track_id_info()

    if track_id not in track_id_info_lookup:
        return None

    artist, title = track_id_info_lookup[track_id]
    return (artist, title)


def main():
    print('hello gmusicplay')
    parser = argparse.ArgumentParser()
    parser.add_argument('track_id', action="store", type=str)
    parser.add_argument('-v', '--verbose', action="store_true", default=False)
    args = parser.parse_args()

    #stream_gmusic_track_blocking(args.track_id, verbose=args.verbose)
    play_gmusic_track_blocking(args.track_id, verbose=args.verbose)


if __name__ == '__main__':
    main()
