import random
import string

import datetime
import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User, File
from api.serializers import UserSerializer, FileUploadSerializer, TokenSerializer
from gambitBackend import settings
from .TokenManager import TokenManger, token_required

"""
============================================================================================
                                AUTHENTICATION
============================================================================================
"""
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
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
    @token_required()
    def post(self, request):
        return Response({"msg": "Successfully logged in"}, status=status.HTTP_200_OK)

"""
============================================================================================
"""


"""
============================================================================================
                                FILE MANIPULATION
============================================================================================
"""
class UploadFile(APIView):
    @token_required()
    def post(self, request):
        data = {
            "jwt": request.data['jwt'],
            "name": request.data['name'],
            "filebase64": request.data['filebase64'],
            "imagebase64": request.data['imagebase64']
        }
        print("got file!")
        fileserializer = FileUploadSerializer(data=data)

        if fileserializer.is_valid():
            token = request.data['jwt']
            tokenmanager = TokenManger(token)

            user = tokenmanager.getUser()
            userid = user.id

            namefile = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
            with open("/home/yggdrasil/gambitDjango/static/" + namefile + ".bs64", "w") as f:
                f.write(request.data['filebase64'])

            nameimage = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
            with open("/home/yggdrasil/gambitDjango/static/" + nameimage + ".bs64", "w") as f:
                f.write(request.data['imagebase64'])


            file = File(name=request.data['name'], userid=userid, fileid=namefile, imageid=nameimage)
            file.save()

            return Response({"succsess": "Uploaded the File!"}, status=status.HTTP_200_OK)
        return Response({"error": f"The File Post was not valid"}, status=status.HTTP_400_BAD_REQUEST)

class GetUserFiles(APIView):
    @token_required()
    def post(self, request):
        token = request.data['jwt']
        tokenserializer = TokenSerializer(data={"jwt": request.data['jwt']})
        if tokenserializer.is_valid():
            tokenmanager = TokenManger(token)
            userid = tokenmanager.getUser().id
            files = File.objects.filter(userid=userid)
            data = {"files": []}
            for file in files.values():
                data['files'].append(file)
            return Response(data, status=status.HTTP_200_OK)
        return Response({"error": f"Something went wrong !"}, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserFile(APIView):
    @token_required()
    def post(self, request):
        token = request.data['jwt']
        tokenserializer = TokenSerializer(data={"jwt": request.data['jwt']})
        if tokenserializer.is_valid():

            tokenmanager = TokenManger(token)
            userid = tokenmanager.getUser().id
            fileid = request.data['fileid']
            file = File.objects.filter(fileid=fileid)
            file = file[0]

            if str(file.userid) == str(userid):
                file.delete()
                return Response({"msg": "File Deleted"}, status=status.HTTP_200_OK)
            return Response({"msg": "The requested file is not yours!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "something went wrong !"}, status=status.HTTP_400_BAD_REQUEST)

class GetJavaCommunicationManagerVersion(APIView):
    def get(self, request):
        return Response({"version": settings.JAVA_COMMUNICATION_MANAGER_VER, "download": settings.JAVA_COMMUNICATION_MANAGER_DOWNLOAD},  status=status.HTTP_200_OK)

"""
============================================================================================
"""
