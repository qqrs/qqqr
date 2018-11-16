import argparse
import requests
import tempfile
import subprocess

from gmusicapi import Mobileclient

import gmusic_secrets

api = None


def init_gmusic_api():
    print('init_gmusic_api')
    global api
    api = Mobileclient()
    logged_in = api.login(gmusic_secrets.USERNAME, gmusic_secrets.PW, Mobileclient.FROM_MAC_ADDRESS)
    assert(logged_in)


def play_mp3_file_blocking(f):
    print('play_mp3_file_blocking')
    subprocess.call(['mpg321', '-q', '-a', 'bluealsa', f.name])


def play_gmusic_track_blocking(track_id, verbose=False):
    if api is None:
        init_gmusic_api()

    print('play_gmusic_track_blocking')
    track_url = api.get_stream_url(track_id, device_id=gmusic_secrets.DEVICE_ID)

    if verbose:
        print(track_url)

    resp = requests.get(track_url)
    resp.raise_for_status()

    with tempfile.NamedTemporaryFile('wb') as f:
        f.write(resp.content)
        play_mp3_file_blocking(f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('track_id', action="store", type=str)
    parser.add_argument('-v', '--verbose', action="store_true", default=False)
    args = parser.parse_args()

    play_gmusic_track_blocking(args.track_id)


if __name__ == '__main__':
    main()
