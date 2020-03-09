#!/bin/sh

echo
echo "\e[92mMEDICAL\e[94mBERRY\e[0m"
echo

pip3 install django==2.2.7
pip3 install django-jet==1.0.8
pip3 install django-allow-cidr==0.3.1
pip3 install libsass==0.19.4
pip3 install feedparser==5.2.1
pip3 install mysqlclient==1.4.6
pip3 install gunicorn==20.0.4

sudo apt-get install nginx
# to do: setup nginx service, make links