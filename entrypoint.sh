#!/bin/bash
echo "Initializing Django server"
cd SRPA
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
