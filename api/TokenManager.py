import jwt
from rest_framework.response import Response

from api.models import User
from api.serializers import UserSerializer
from gambitBackend import settings


class TokenManger:
    """
    Attributes
    ----------
    Token : str
        User sends token to this class. The class verifies the token

    User: User
        When the token is verifed it askes the db for the user and saves it to this field
        for later use

    Methods
    -------
     validate():
        Validates the token. Saves the user in class
        return boolean whether successful or not

    getUser():
        getter for the user
        return self.user

    getSerializer():
        getter for the serializer. Serializer has more methods and ensures the data we get
        from the db is valid.
        return self.serializer

    isValid():
        function to check if the last token check was valid or not.
        With that you have to only check once for each token and can asume that
        you have a valid user also.
        return self.valid
    """

    def __init__(self, token):
        """
        Only needs the token

        Parameters
        ----------
        token : str
            the token in string format
        """
        self.token = token
        self.user = None
        self.serializer = None
        self.valid = self.validate()


    def validate(self):
        """
        Validates the JWT token. Uses the SECRET_KEY specified in the Settings.py
        See Docs Introduction for further details

        Returns
        -------
            boolean whether successful or not
        """
        try:
            payload = jwt.decode(self.token, settings.SECRET_KEY, algorithms=['HS256'])
        except:
            return False

        self.serializer = UserSerializer(User.objects.filter(id=payload['id']).first())
        self.user = User.objects.filter(id=payload['id']).first()

        return True

    def getUser(self):
        """
        Getter for the user. Always ensure there is one with isVerified()

        Returns
        -------
           returns the user
        """
        return self.user

    def getSerializer(self):
        """
        Getter for the serializer. Always ensure there is one with isVerified()

        Returns
        -------
            returns the serializer
        """
        return self.serializer

    def isValid(self):
        """
        Shows if the last validation was successful or not

        Returns
        -------
            boolean whether successful or not
        """
        return self.valid

def token_required():
    """
    Decorator that checks if a token is valid.
    Can be used with python views
    """
    def wrapper(view_func):
        def wrapped(request, *args, **kwargs):
            token = args[0].data['jwt']
            jwtManage = TokenManger(token)
            if not token:
                return Response({'iserror': '1', 'error': 'Missing jwt', 'jwt': ''}, 401)

            if not jwtManage.isValid():
                return Response({'iserror': '1', 'error': 'Invalid token', 'jwt': ''}, 401)
            else:
                return view_func(request, *args, **kwargs)
        return wrapped
    return wrapper