from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(UserTokenObtainPairSerializer, cls).get_token(user)
        return token

    def validate(cls, attrs):
        data = super(UserTokenObtainPairSerializer, cls).validate(attrs)

        refresh = cls.get_token(cls.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        roles = list(set([x.name for x in cls.user.groups.all()]))
        if "app_user" in roles:
            data["role"] = "app_user"

        elif cls.user.is_superuser:
            data["role"] = "superuser"
        else:
            data["role"] = "user"

        return data


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
