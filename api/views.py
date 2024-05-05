import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User
from api.serializers import UserSerializer, FileSerializer
import jwt, datetime

from gambitBackend import settings


# Create your views here.

class TokenManger:
    def __init__(self, token):
        self.token = token
        self.user = None
        self.serializer = None
        self.valid = self.validate()


    def validate(self):
        try:
            payload = jwt.decode(self.token, settings.SECRET_KEY, algorithms=['HS256'])
        except:
            return False

        self.serializer = UserSerializer(User.objects.filter(id=payload['id']).first())
        self.user = User.objects.filter(id=payload['id']).first()

        return True

    def getUser(self):
        return self.user

    def getSerializer(self):
        return self.serializer

    def isValid(self):
        return self.valid


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        print(str(request.data))
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is not None and user.check_password(password):

            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=60),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            return Response({"jwt": token}, status=status.HTTP_200_OK)
        return Response({"error": "Login Failed"}, status=status.HTTP_400_BAD_REQUEST)

class CheckIfAuthenticated(APIView):
    def post(self, request):
        token = request.data['jwt']
        tokenmanager = TokenManger(token)
        if(tokenmanager.isValid()):
            return Response(tokenmanager.getSerializer().data, status=status.HTTP_200_OK)
        return Response({"error": f"Please log in again your token: {token} is not valid"}, status=status.HTTP_400_BAD_REQUEST)

class UploadFile(APIView):
    def post(self, request):
        token = request.data['jwt']
        tokenmanager = TokenManger(token)
        if(tokenmanager.isValid()):
            data = {
                "user": tokenmanager.getUser(),
                "name": request.data['name'],
                "base64": request.data['base64'],
            }

            fileserializer = FileSerializer(data=data)
            if fileserializer.is_valid():
                fileserializer.save()
                return Response(fileserializer, status=status.HTTP_200_OK)
        return Response({"error": f"Please log in again your token: {token} is not valid"}, status=status.HTTP_400_BAD_REQUEST)


class GetJavaCommunicationManagerVersion(APIView):
    def get(self, request):
        return Response({"version": settings.JAVA_COMMUNICATION_MANAGER_VER},  status=status.HTTP_200_OK)
