import json
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import UserRegistrationSerializer
import requests
from rest_framework.permissions import AllowAny
from django.urls import reverse


class JoinView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            if not User.objects.filter(username=username).exists():
                User.objects.create_user(**serializer.validated_data)

            headers = {"Content-Type": "application/json"}
            data = {
                "username": username,
                "password": password,
            }
            url = request.build_absolute_uri(reverse("token_obtain_pair"))
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                response = response.json()
                print(response)
                return Response(
                    {"access_token": response["access"]},
                    status=status.HTTP_200_OK,
                )
            elif response.status_code == 401:
                return Response({"error": "Invalid Credentials."})
            else:
                return Response({"error": "Something went wrong."})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
