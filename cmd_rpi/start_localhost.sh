#!/bin/sh

echo
echo "\e[92mMEDICAL\e[94mBERRY\e[0m"
echo

cd `dirname $0`
cd ..

python3 manage.py runserver