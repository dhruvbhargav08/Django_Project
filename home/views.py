from django.shortcuts import render
from .models import Student,Teacher,Student_Teacher_Relation
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
        role = request.data.get('role')
        if not email or not password or not name or not role:
            response={
                "message": "missing Input"
            }
            return Response(response,status.HTTP_400_BAD_REQUEST)
        enc_pass = pbkdf2_sha256.encrypt(password, rounds = 12000, salt_size = 32)
        if role=='teacher':
            subject = request.data.get('subject')
            user_instance = Teacher.objects.create(
                email=email,
                password=enc_pass,
                name=name,
                subject=subject
            )
        elif role=='student':
            standard = request.data.get('standard')
            user_instance = Student.objects.create(
                email=email,
                password=enc_pass,
                name=name,
                standard=standard
            )
        user_instance.save()
        response = {"message": "user created successfully"}
        return Response(response, status=status.HTTP_201_CREATED)

class Get_All_Student(APIView):
    def get(self,request):
        students = Student.objects.all()
        student_data = []
        for student in students:
            student_dict = {
                'email': student.email,
                'name': student.name,
                'standard': student.standard
            }
            student_data.append(student_dict)
        response = {
            'students': student_data
        }
        return Response(response, status=status.HTTP_200_OK)

class Get_All_Teacher(APIView):
    def get(self,request):
        teachers = Teacher.objects.all()
        teacher_data = []
        for teacher in teachers:
            teacher_dict = {
                'email': teacher.email,
                'name': teacher.name,
                'subject': teacher.subject
            }
            teacher_data.append(teacher_dict)
        response = {
            'teachers': teacher_data
        }
        return Response(response, status=status.HTTP_200_OK)

class Update_Student(APIView):
    def put(self,request):
        email = request.data.get('email')
        name = request.data.get('name')
        standard = request.data.get('standard')
        if not email or not name:
            response={
                "message": "missing Input"
            }
            return Response(response,status.HTTP_400_BAD_REQUEST)
        student = Student.objects.filter(email=email).first()
        if student==None:
            response = {
                "message": "no student found"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        student.name = name
        student.standard = standard
        student.save()
        student = Student.objects.filter(email=email).first()
        student_data = []
        student_dict = {
            'email': student.email,
            'name': student.name,
            'standard': student.standard
        }
        student_data.append(student_dict)
        response = {
            'students': student_data
        }
        return Response(response, status=status.HTTP_200_OK)
    
class Update_Teacher(APIView):
    def put(self,request):
        email = request.data.get('email')
        name = request.data.get('name')
        subject = request.data.get('subject')
        if not email or not name:
            response={
                "message": "missing Input"
            }
            return Response(response,status.HTTP_400_BAD_REQUEST)
        teacher = Teacher.objects.filter(email=email).first()
        if teacher==None:
            response = {
                "message": "no teacher found"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        teacher.name = name
        teacher.subject = subject
        teacher.save()
        teacher = Teacher.objects.filter(email=email).first()
        teacher_data = []
        teacher_dict = {
            'email': teacher.email,
            'name': teacher.name,
            'subject': teacher.subject
        }
        teacher_data.append(teacher_dict)
        response = {
            'teachers': teacher_data
        }
        return Response(response, status=status.HTTP_200_OK)

class Delete_Teacher(APIView):
    def delete(self,request):
        email = request.data.get('email')
        if not email:
            response={
                "message": "missing Input"
            }
            return Response(response,status.HTTP_400_BAD_REQUEST)
        teacher = Teacher.objects.filter(email=email).first()
        if teacher==None:
            response = {
                "message": "no teacher found"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        teacher_data = []
        teacher_dict = {
            'email': teacher.email,
            'name': teacher.name,
            'subject': teacher.subject
        }
        teacher_data.append(teacher_dict)
        teacher.delete()
        response = {
            'teachers': teacher_data
        }
        return Response(response, status=status.HTTP_200_OK)

class Delete_Student(APIView):
    def delete(self,request):
        email = request.data.get('email')
        if not email:
            response={
                "message": "missing Input"
            }
            return Response(response,status.HTTP_400_BAD_REQUEST)
        student = Student.objects.filter(email=email).first()
        if student==None:
            response = {
                "message": "no student found"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        student_data = []
        student_dict = {
            'email': student.email,
            'name': student.name,
            'standard': student.standard
        }
        student_data.append(student_dict)
        student.delete()
        response = {
            'students': student_data
        }
        return Response(response, status=status.HTTP_200_OK)
    
class Assign_Student_Teacher(APIView):
    def post(self,request):
        student_email = request.data.get('student')
        teacher_email = request.data.get('teacher')
        if not student_email or not teacher_email:
            response = {
                "message": "missing input"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        student = Student.objects.filter(email=student_email).first()
        teacher = Teacher.objects.filter(email=teacher_email).first()
        if not student:
            response = {
                "message": "student not found"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if not teacher:
            response = {
                "message": "teacher not found"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        Student_Teacher_Relation.objects.create(student_id=student.email,teacher_id=teacher.email)
        response = {
            "message": "relation created successfully"
        }
        return Response(response, status=status.HTTP_201_CREATED)
