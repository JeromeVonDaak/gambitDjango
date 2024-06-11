# How to install
### Dependencies
```python
pip install django
pip install djangorestframework
pip install markdown
pip install django-filter
pip install django[argon2]
```
### First Start
```python
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
# Instructions
### Starting the app
```
python manage.py runserver
```

\documentclass[titlepage]{article}
\author{Jérome von Daak}
\title{Dokumentation von Backend und CommunicationModule}

\usepackage{markdown}
\usepackage[ngerman]{babel}
\usepackage{minted}

\begin{document}
\maketitle
\tableofcontents
\newpage
\begin{markdown}
# Backend
## Overview
Ziel dieses Backends ist es dem User eine Möglichkeit zum registrieren und anmelden zu bieten. Er soll ebenfalls fähig sein Dateien hoch und runterzuladen. Um diese Funktionen zu gewährleisten, haben wir uns für folgenden Backend-Stack entschieden.

### Django
Django ist das genutze Backend Framework. Das Framework behandelt Registrieren, Login, sowie hoch und runterladen von Dateien. Zur clientenkommunikation wird eine api verwendet.

- [siehe Django Docs](https://docs.djangoproject.com/en/5.0/)
- [siehe Django REST Framework (für die Api)](https://www.django-rest-framework.org/)


### Gunicorn
Gunicorn served das Backend. Es macht das Core Backend im Netzwerk sichtbar. Django´s eigener Webserver gilt als nicht sicher weswegen ein andere Webserver wie Gunicorn empfehlenswert ist.

- [siehe Gunicorn Docs](https://docs.gunicorn.org/en/stable/)

### http-server
Zum Bereitstellen von Files. Gunicorn bietet hier keinen guten fileserver, weswegen wir uns für http-server entschieden haben.

- [siehe http-server Docs](https://github.com/http-party/http-server)

### Nginx
Bildet die Schnittstelle zwischen dem Internet und dem Backend. Proxied den Traffic an die richtigen Server. Gewähleistet auserdem ssl Verschlüsselung.

- [siehe Nginx Docs](https://nginx.org/en/docs/)

### Cloudflare
Stellt die nötigen SSL Zertifikate zur Verfügung. Bieten zusätzlichen Schutz vor DDOS Attacken. Cached Datein und beschleunigt so download für den Clienten.

\end{markdown}
\newpage
\begin{markdown}
## Installation
Bei der Installation vom Backend gibt es einige schritte zu beachten.

### Installation Core
### Installation Gunicorn
### Installation Http-server
### Installation Nginx

\end{markdown}
\begin{minted}
[
frame=lines,
framesep=2mm,
baselinestretch=1.2,
fontsize=\footnotesize,
linenos
]
{python}
\end{minted}

\newpage
\begin{markdown}
## Klassen Overview
Im folgendem behandeln wir alle Wichtigen Klassen des Backends

### Views.py
In Views.py werden alle Http Anfragen verarbeiten. Hier wird definiert wie auf eine Anfrage geantworted wird.


### Models.py
In Models.py wird das Datenbank Schema definiert. Django kann dann im gesamten Projekt die definierten Datenbank Objekte hernehmen.

\end{markdown}
\begin{minted}
[
frame=lines,
framesep=2mm,
baselinestretch=1.2,
fontsize=\footnotesize,
linenos
]
{python}
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
# Create your models here.

# User Model to Login and auth
class User(AbstractUser):
name = models.CharField(max_length=255)
email = models.EmailField(unique=True)
password = models.CharField(max_length=255)
username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class File(models.Model):
# id of the file itself
id = models.BigAutoField(primary_key=True, auto_created=True)
# the display name of the file
name = models.CharField(max_length=255)
# the owner of the file
userid = models.CharField(max_length=255)
# the cover imageid that links to the base64 image
imageid = models.CharField(max_length=255)

    # the fileid that links to the base64 file
    fileid = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Filebase(models.Model):
id = models.BigAutoField(primary_key=True, auto_created=True)
base64 = models.TextField()

    def __str__(self):
        return self.id

class Imagebase(models.Model):
id = models.BigAutoField(primary_key=True, auto_created=True)
base64 = models.TextField()

    def __str__(self):
        return self.id
\end{minted}
\begin{markdown}

### Urls.py
In Urls.py wird definiert, welche Urls mit welcher View verbunden sind.
\end{markdown}
\begin{minted}
[
frame=lines,
framesep=2mm,
baselinestretch=1.2,
fontsize=\footnotesize,
linenos
]
{python}
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
path('register/', RegisterView.as_view(), name='register'),
path('login/', LoginView.as_view(), name='login'),
path('checkvalid/', CheckIfAuthenticated.as_view(), name='checkvalid'),
path('uploadfile/', UploadFile.as_view(), name='uploadfile'),
path('getuserfiles/', GetUserFiles.as_view(), name='getuserfiles'),
path('checkcommunicationmanagerversion/', GetJavaCommunicationManagerVersion.as_view(), name='checkcommunicationmanagerversion')
]

\end{minted}
\begin{markdown}
### Serializers.py
In Serializer.py wird definiert welche Parameter das Backend annimmt. Auserdem wandeln Serializer json in leicht python lesbaren Code um.
\end{markdown}
\begin{minted}
[
frame=lines,
framesep=2mm,
baselinestretch=1.2,
fontsize=\footnotesize,
linenos
]
{python}
from rest_framework import serializers
from api.models import User, File

class UserSerializer(serializers.ModelSerializer):
class Meta:
model = User
fields = ['id', 'name', 'email', 'password']

        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}
        }

    # For Hashing the password
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class FileUploadSerializer(serializers.Serializer):
name = serializers.CharField()
jwt = serializers.CharField()
imagebase64 = serializers.CharField()
filebase64 = serializers.CharField()

class FileSerializer(serializers.ModelSerializer):
class Meta:
model = File
fields = '__all__'

class TokenSerializer(serializers.Serializer):
jwt = serializers.CharField()
\end{minted}
\begin{markdown}
# Communication Module

## Overview
Das Communication Module verbindet das Backend mit dem Java Frontend. Es behandelt alle Anfragen die an den Server gehen sollen: Login, Register, Upload File, Download File, GetAllUserFiles

## Klassen Overview


\end{markdown}
\end{document}


\end{markdown}
\begin{minted}
[
frame=lines,
framesep=2mm,
baselinestretch=1.2,
fontsize=\footnotesize,
linenos
]
{python}
\end{minted}