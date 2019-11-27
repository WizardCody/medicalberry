#!/bin/sh

echo
echo "\e[92mMEDICAL\e[94mBERRY\e[0m"
echo

sudo apt-get update
sudo apt-get install libglib2.0-dev

pip3 install bluepy==1.3.0
pip3 install pycrypto==2.6.1