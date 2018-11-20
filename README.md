# QQQR: qr-code music player

## Raspberry Pi config

#### Wi-Fi config

https://learn.adafruit.com/raspberry-pi-zero-creation/text-file-editing

## OpenCV installation

#### ROSbots

SD card image with precompiled OpenCV binaries

https://medium.com/@rosbots/ready-to-use-image-raspbian-stretch-ros-opencv-324d6f8dcd96

https://github.com/ROSbots/rosbots_setup_tools#use-our-existing-rosbots-raspbianrosopencv-image-after-youve-downloaded-it

#### PyImageSearch

Instructions for compiling OpenCV on Raspberry Pi. Takes 24+ hours on Raspberry Pi Zero!

https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/

## Bluetooth speaker

#### Pairing Bluetooth speaker

https://www.sigmdel.ca/michel/ha/rpi/bluetooth_01_en.html

https://gist.github.com/actuino/9548329d1bba6663a63886067af5e4cb

#### Reconnect Bluetooth speaker

```
bluetoothctl -a
connect C0:28:8D:02:8D:8E
quit
```

#### Play a test wav

```
aplay -D bluealsa:HCI=hci0,DEV=C0:28:8D:02:8D:8E,PROFILE=a2dp /usr/share/sounds/alsa/Front_Center.wav
```

#### Configure `.asoundrc`

```
pi@qqpi:~ $ cat .asoundrc
defaults.bluealsa.interface "hci0"
defaults.bluealsa.device "C0:28:8D:02:8D:8E"
defaults.bluealsa.profile "a2dp"
```

#### Auto-connect Bluetooth speaker

https://raspberrypi.stackexchange.com/a/53456
https://raspberrypi.stackexchange.com/a/53745

## streaming mp3 playback

#### mplayer

https://www.raspberrypi.org/forums/viewtopic.php?t=189323

## Mopidy (no longer used)

#### mopidy installation

```
sudo apt remove python-pip
wget -q https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py

sudo apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev
sudo apt-get install python-lxml
pip install mopidy-gmusic
sudo pip install mopidy-gmusic --ignore-installed pyasn1 --ignore-installed lxml
```

#### mopidy config

```
pi@qqpi:~ $ vi ~/.config/mopidy/mopidy.conf
[audio]
#mixer = software
#mixer_volume =
output = alsasink device = bluealsa
#buffer_time =

[http]
#enabled = true
#hostname = 127.0.0.1
hostname = ::

[local]
#enabled = true
#library = json
media_dir = /home/pi/bluetooth_audio
```

#### control via mpd client

```
mpc add local:track:Untitled3.wav && mpc repeat && mpc play
mpc ls 'Google Music/Albums/The Grateful Dead - 5-8-77'
mpc add gmusic:track:7649c1b0-9499-36ef-bfe4-4f2a121ac08a && mpc play
```
