#!/bin/bash

if [ "$DEBUG"==True ]; then
    python manage.py makemigrations
    python manage.py migrate
    python manage.py load_all_data
    python manage.py collectstatic --no-input
fi

gunicorn foodgram.wsgi:application --bind 0:8000