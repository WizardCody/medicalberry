#!/bin/sh

echo
echo "\e[92mMEDICAL\e[94mBERRY\e[0m"
echo

pip3 install django
pip3 install django-jet
pip3 install libsass
pip3 install feedparser
pip3 install mysqlclient
pip3 install django-allow-cidr
pip3 install gunicorn

sudo apt-get install nginx
# to do: setup nginx service, make links