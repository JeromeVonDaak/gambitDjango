from django.urls import path
from .views import *

urlpatterns = [
    path('checkvalid/', CheckIfAuthenticated.as_view(), name='checkvalid'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path('uploadfile/', UploadFile.as_view(), name='uploadfile'),
    path('deletefile/', DeleteUserFile.as_view(), name='deletefile'),
    path('getuserfiles/', GetUserFiles.as_view(), name='getuserfiles'),

    path('checkcommunicationmanagerversion/', GetJavaCommunicationManagerVersion.as_view(), name='checkcommunicationmanagerversion')
]
