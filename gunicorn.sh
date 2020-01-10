#!/bin/sh

echo
echo "\e[92mMEDICAL\e[94mBERRY\e[0m"
echo

gunicorn --bind unix:/home/pi/Desktop/medicalberry/gunicorn.sock medicalberry.wsgi