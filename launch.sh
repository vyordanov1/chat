#!/bin/sh
pip3 install -r requirements.txt
cd app
#
python3 manage.py collectstatic --noinput
#
# Migrate
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver 0.0.0.0:8000
