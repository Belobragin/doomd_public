#!/usr/bin/bash

#initial script for AWS lightsail django instances
sudo su <<HERE
apt-get update ##[edited]
apt-get install ffmpeg libsm6 libxext6  -y
apt-get install build-essential python-dev
apt-get install uwsgi
apt-get install uwsgi-plugin-python3

HERE

exit $?