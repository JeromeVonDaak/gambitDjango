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

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = 'user, name, base64'
        extra_kwargs = {
            "base64": {"write_only": True}
        }
