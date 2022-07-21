# base image
FROM python:3.7-bullseye

# set environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# webapp directory im Container erstellen und als working directory festlegen
WORKDIR /webapp

# copy whole project to your docker home directory. 
COPY . /webapp/

# Datenbanknutzer und Datenbank erstellen
#COPY init.sql /docker-entrypoint-initdb.d/

# upgrade pip (optional?)  
RUN pip install --upgrade pip  

#let pip install required packages
RUN pip install -r requirements.txt

# Gunicorn as app server
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 stars.wsgi:application