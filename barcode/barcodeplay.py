import time
import logging
import argparse
import subprocess

from imutils.video import VideoStream
from pyzbar import pyzbar
import gmusicplay


log = logging
QQQR_ROOT_URI = 'qqqr:gmusic:track:'


def init():
    log.debug('init')
    t0 = time.time()

    # Initialize video stream.
    vs = VideoStream(usePiCamera=True).start()

    # Initialize Google Play Music api.
    gmusicplay.init_gmusic_api()

    # Ensure camera sensor has had time to warm up.
    while time.time() - t0 < 2.0:
        time.sleep(0.1)

    return vs


def cleanup(vs):
    log.debug('cleanup')
    vs.stop()


def play_buzz():
    """Play a sound to indicate success"""
    subprocess.call(['aplay', '-D', 'bluealsa', '/usr/share/sounds/alsa/Noise.wav'])


def scan_barcodes_loop(vs, tmax=1200):
    log.debug('scan_barcodes_loop')
    log.info('Ready for barcodes...')
    t0 = time.time()

    while True:
        tf = time.time()
        if tf - t0 > tmax:
            return None

        # Get a frame of video.
        frame = vs.read()

        # Detect barcodes in the frame.
        barcodes = pyzbar.decode(frame)

        log.debug("Scanned new frame in %0.2fs" % (time.time() - tf))

        if barcodes:
            return barcodes


def parse_qqqr_barcode(barcode):
    log.info('parse_qqqr_barcode')
    if barcode.type != 'QRCODE':
        raise Exception('Unexpected barcode type: %s' % barcode.type)

    data = barcode.data.decode('utf-8')
    log.info('Found barcode: %s: %s' % (barcode.type, data))

    if not data.startswith(QQQR_ROOT_URI):
        raise Exception('Unexpected QR data: %s' % data)

    track_id = data[len(QQQR_ROOT_URI):]
    return track_id


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="store_true", default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    vs = init()

    while True:
        play_buzz()
        barcodes = scan_barcodes_loop(vs, tmax=1200)
        if not barcodes:
            # Timed out without detecting a barcode.
            break

        play_buzz()

        if len(barcodes) > 1:
            log.warning('detected multiple barcodes in frame')

        track_id = parse_qqqr_barcode(barcodes[0])
        gmusicplay.play_gmusic_track_blocking(track_id)

    cleanup(vs)


if __name__ == '__main__':
    main()
