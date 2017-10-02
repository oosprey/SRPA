#!/bin/bash
echo "Initializing Django server"
cd SRPA
python manage.py migrate
uwsgi --ini web/SRPA_uwsgi.ini :8000
