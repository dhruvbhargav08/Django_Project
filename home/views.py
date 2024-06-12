from django.shortcuts import render
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView,Response
from passlib.hash import pbkdf2_sha256
# Create your views here.

class Add_User(APIView):
    def post(self, request):
        email = request.data.get('email')
        name = request.data.get('name')
        password = request.data.get('password')
        if not email or not password or not name:
            response={
                "message": "Missing Input"
            }
            return Response(response,status.HTTP_400_BAD_REQUEST)
        enc_pass = pbkdf2_sha256.encrypt(password, rounds = 12000, salt_size = 32)
        user_instance = User.objects.create(
            email=email,
            password=enc_pass,
            name=name,
        )
        user_instance.save()
        response = {"message": "User created successfully"}
        return Response(response, status=status.HTTP_201_CREATED)

class Get_All_User(APIView):
    def get(self,request):
        users = User.objects.all()
        user_data = []
        for user in users:
            user_dict = {
                'email': user.email,
                'name': user.name
            }
            user_data.append(user_dict)
        response = {
            'users': user_data
        }
        return Response(response, status=status.HTTP_200_OK)

class Get_User(APIView):
    def get(self,request):
        email = request.data.get('email')
        if not email:
            response={
                "message": "Missing Input"
            }
            return Response(response,status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email)
        user_data = []
        for user in user:
            user_dict = {
                'email': user.email,
                'name': user.name
            }
            user_data.append(user_dict)
        response = {
            'users': user_data
        }
        if len(user_data)==0:
            response = {
                'message': 'no user found'
            }
        return Response(response, status=status.HTTP_200_OK)

class Update_User(APIView):
    def put(self,request):
        email = request.data.get('email')
        name = request.data.get('name')
        if not email or not name:
            response={
                "message": "Missing Input"
            }
            return Response(response,status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if user==None:
            response = {
                "message": "no user found"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        user.name = name
        user.save()
        user = User.objects.filter(email=email).first()
        user_data = []
        user_dict = {
            'email': user.email,
            'name': user.name
        }
        user_data.append(user_dict)
        response = {
            'users': user_data
        }
        return Response(response, status=status.HTTP_200_OK)

class Delete_User(APIView):
    def delete(self,request):
        email = request.data.get('email')
        if not email:
            response={
                "message": "Missing Input"
            }
            return Response(response,status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if user==None:
            response = {
                "message": "no user found"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        user_data = []
        user_dict = {
            'email': user.email,
            'name': user.name
        }
        user_data.append(user_dict)
        user.delete()
        response = {
            'users': user_data
        }
        return Response(response, status=status.HTTP_200_OK)