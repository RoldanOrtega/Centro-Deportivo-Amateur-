#!/bin/sh
source .venv/bin/activate
python CentroDeportivo/manage.py runserver $PORT
