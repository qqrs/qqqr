from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import cv2
import time

import gmusicplay

QQQR_ROOT_URI = 'qqqr:gmusic:track:'

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")

vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

print("[INFO] starting loop...")

# loop over the frames from the video stream
i = 0
while True:
    start = time.time()
    # grab the frame from the threaded video stream and resize it to
    # have a maximum width of 400 pixels
    frame = vs.read()
    #frame = imutils.resize(frame, width=400, inter=cv2.INTER_CUBIC)
    #cv2.imwrite('%00d.jpg' % i, frame)
    i += 1
 
    # find the barcodes in the frame and decode each of the barcodes
    barcodes = pyzbar.decode(frame)
    end = time.time()

    print("[INFO] new frame in %0.2fs" % (end-start))

    if barcodes:
        break


if barcodes:
    barcode = barcodes[0]
    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type
    print('found: %s: %s' % (barcodeType, barcodeData))

    if not barcodeData.startswith(QQQR_ROOT_URI):
        raise Exception('Unexpected QR data: %s' % barcodeData)

    track_id = barcodeData[len(QQQR_ROOT_URI):]

    gmusicplay.play_gmusic_track_blocking(track_id)

    #time.sleep(0.3)


print("[INFO] cleaning up...")
vs.stop()
