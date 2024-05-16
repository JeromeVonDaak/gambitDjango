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
