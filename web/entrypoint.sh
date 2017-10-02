#!/bin/bash
echo "Initializing Django server"
cd SRPA
echo "Pulling new changes from git repository"
git pull
echo "Migrating databases"
python manage.py migrate
echo "Starting uwsgi"
uwsgi --ini web/SRPA_uwsgi.ini
