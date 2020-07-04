#!/bin/bash

apt-get install ffmpeg --assume-yes
apt-get install libzbar-dev libzbar0 --assume-yes
apt-get install build-essential python3-dev git scons swig --assume-yes
apt-get install libffi-dev --assume-yes

#python3 -m pip install -U discord.py[voice]