#!/bin/sh
pip3 install -r requirements.txt
cd app
#
python3 manage.py collectstatic --noinput
#
# Migrate
python3 manage.py makemigrations
python3 manage.py migrate

#python3 manage.py runserver 0.0.0.0:8000
daphne -b 0.0.0.0 -p 8000 app.asgi:application --websocket_timeout -1 --websocket_connect_timeout 100