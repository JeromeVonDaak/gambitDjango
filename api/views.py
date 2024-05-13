import json

from django.shortcuts import render
from django.core import serializers
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User, Filebase, Imagebase, File
from api.serializers import UserSerializer, FileUploadSerializer, FileSerializer, TokenSerializer
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

class FileUploader:
    def __init__(self, file):
        self.file = file


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
        data = {
            "jwt": request.data['jwt'],
            "name": request.data['name'],
            "filebase64": request.data['filebase64'],
            "imagebase64": request.data['imagebase64']
        }
        fileserializer = FileUploadSerializer(data=data)

        if fileserializer.is_valid():
            token = request.data['jwt']
            tokenmanager = TokenManger(token)

            user = tokenmanager.getUser()
            userid = user.id


            filebase = Filebase(base64=request.data['filebase64'])
            filebase = filebase.save()
            filebaseid = Filebase.objects.latest('id').id

            imagebase = Imagebase(base64=request.data['imagebase64'])
            imagebase = imagebase.save()
            imagebaseid = Imagebase.objects.latest('id').id

            print(f'filebaseid: {filebaseid}, imagebaseid: {imagebaseid}')
            file = File(name=request.data['name'], userid=userid, fileid=filebaseid, imageid=imagebaseid)
            file.save()

            if tokenmanager.isValid():
                return Response(fileserializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": f"Please log in again your token: {token} is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": f"The File Post was not valid"}, status=status.HTTP_400_BAD_REQUEST)

class GetUserFiles(APIView):
    def post(self, request):
        token = request.data['jwt']
        tokenmanager = TokenManger(token)
        tokenserializer = TokenSerializer(data={"jwt": request.data['jwt']})
        if tokenserializer.is_valid() and tokenmanager.isValid():
            userid = tokenmanager.getUser().id
            print(userid)
            files = File.objects.filter(userid=userid)
            print(files.values())
            data = {"files": []}
            for file in files.values():
                data['files'].append(file)
            return Response(data, status=status.HTTP_200_OK)
        return Response({"error": f"Something went wrong !"}, status=status.HTTP_400_BAD_REQUEST)

class GetFile(APIView):
    def post(self, request):
        print(request.data['jwt'])
        token = request.data['jwt']
        fileid = int(request.data['fileid'])
        tokenmanager = TokenManger(token)
        tokenserializer = TokenSerializer(data={"jwt": request.data['jwt']})
        if tokenserializer.is_valid() and tokenmanager.isValid() and fileid.is_integer():
            userid = tokenmanager.getUser().id
            file = File.objects.get(fileid=fileid)
            # Checks if the User owns the File
            print(f'fileid: {file.userid}/userid: {userid}')
            if int(file.userid) == userid:
                # the base64 of the file
                filebase = Filebase.objects.get(id=fileid)
                # the base64 of the image
                coverimage = Imagebase.objects.get(id=fileid)
                data = {'filename': file.name, 'filebase': filebase.base64, 'imagebase': coverimage.base64}
                return Response(data, status=status.HTTP_200_OK)
        return Response({"error": f"Something went wrong !"}, status=status.HTTP_400_BAD_REQUEST)


class GetJavaCommunicationManagerVersion(APIView):
    def get(self, request):
        return Response({"version": settings.JAVA_COMMUNICATION_MANAGER_VER, "download": settings.JAVA_COMMUNICATION_MANAGER_DOWNLOAD},  status=status.HTTP_200_OK)
