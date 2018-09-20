#!/bin/bash
python3 django/manage.py migrate
python3 django/manage.py runserver 0.0.0.0:8000
