#!/bin/sh

echo
echo "\e[92mMEDICAL\e[94mBERRY\e[0m"
echo

rm -f ./db.sqlite3
rm -f ./heartguard/migrations/*.py
touch ./heartguard/migrations/__init__.py
rm -f ./homeguard/migrations/*.py
touch ./homeguard/migrations/__init__.py

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser