#!/usr/bin/env bash

python /code/django_sensors/manage.py runserver & # server
P1=$!
cd /code/vue-project && npm run dev & # vue frontend
P2=$!
wait $P1 $P2