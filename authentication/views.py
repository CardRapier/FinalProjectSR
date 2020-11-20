from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
from django.contrib import auth
import jwt
# Create your views here.


@api_view(['GET'])
def authOverview(request):
    api_urls = {
        'Create': '/registration/',
    }

    return Response(api_urls)


@api_view(['POST'])
def userCreate(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = {'user': {
            "id": serializer.data['id'], "username": serializer.data['username']}}
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['POST'])
def userLogin(request):
    data = request.data
    username = data.get('username', '')
    password = data.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user:
        auth_token = jwt.encode(
            {'username': user.username}, settings.JWT_SECRET_KEY)
        serializer = UserSerializer(user)
        data = {'user': {
            "id": serializer.data['id'], "username": serializer.data['username']}, 'token': auth_token}
        return Response(data, status=status.HTTP_200_OK)

    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
