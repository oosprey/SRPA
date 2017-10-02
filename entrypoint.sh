#!/bin/bash
echo "Initializing Django server"
cd SRPA
python manage.py migrate
uwsgi --ini SRPA_uwsgi.ini
