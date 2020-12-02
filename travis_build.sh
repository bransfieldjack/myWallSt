#!/bin/sh
cd backend
pip install requirements.txt
python python manage.py test

# language: python
#     python: 
#       - "3.9"
#     services: 
#       - postgres
#     env: 
#       -DJANGO=3.1.3 DB=postgres
#     install: 
#       - pip install -r requirements.txt
#     script: 
#       - python manage.py test