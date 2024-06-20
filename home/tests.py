from rest_framework import status
from rest_framework.test import APITestCase
from .models import Student, Teacher

class UserTests(APITestCase):
    def test_create_teacher(self):
        url = '/add_user'
        data = {
            'email': 'teacher@example.com',
            'name': 'Teacher Name',
            'password': 'teacherpass',
            'role': 'teacher',
            'subject': 'Mathematics'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.count(), 1)
        self.assertEqual(Teacher.objects.get().email, 'teacher@example.com')

    def test_create_student(self):
        url = '/add_user'
        data = {
            'email': 'student@example.com',
            'name': 'Student Name',
            'password': 'studentpass',
            'role': 'student',
            'standard': 10
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.get().email, 'student@example.com')

    def test_create_user_missing_input(self):
        url = '/add_user'
        data = {
            'email': 'incomplete@example.com',
            'name': 'Incomplete User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "missing Input")

    def test_get_all_students(self):
        Student.objects.create(email='student1@example.com', name='Student Name One', standard=10)
        Student.objects.create(email='student2@example.com', name='Student Name Two', standard=12)
        url = '/get_all_student'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['students']), 2)

    def test_get_all_teachers(self):
        Teacher.objects.create(email='teacher1@example.com', name='Teacher Name One', subject='Math')
        Teacher.objects.create(email='teacher2@example.com', name='Teacher Name Two', subject='Science')
        url = '/get_all_teacher'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['teachers']), 2)

    def test_update_student(self):
        student = Student.objects.create(email='student@example.com', name='Student Old Name', standard=10)
        url = '/update_student'
        data = {
            'email': 'student@example.com',
            'name': 'New Name',
            'standard': 11
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        student.refresh_from_db()
        self.assertEqual(student.name, 'New Name')
        self.assertEqual(student.standard, 11)

    def test_update_teacher(self):
        teacher = Teacher.objects.create(email='teacher@example.com', name='Teacher Old Name', subject='English')
        url = '/update_teacher'
        data = {
            'email': 'teacher@example.com',
            'name': 'New Name',
            'subject': 'Maths'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        teacher.refresh_from_db()
        self.assertEqual(teacher.name, 'New Name')
        self.assertEqual(teacher.subject, 'Maths')
    
    def test_delete_teacher_success(self):
        Teacher.objects.create(email="teacher@example.com", name="Teacher Name One", subject="Math")
        url = '/delete_teacher'
        data = {
            'email': 'teacher@example.com'
        }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['teachers']), 1)

    def test_delete_teacher_missing_email(self):
        url = '/delete_teacher'
        data = {

        }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "missing Input")

    def test_delete_teacher_not_found(self):
        url = '/delete_teacher'
        data = {
            'email': 'nonexistent@example.com'
            }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "no teacher found")
        
    def test_delete_student_success(self):
        Student.objects.create(email="student@example.com", name="student Name One", standard=10)
        url = '/delete_student'
        data = {
            'email': 'student@example.com'
        }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['students']), 1)

    def test_delete_student_missing_email(self):
        url = '/delete_student'
        data = {
        }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "missing Input")

    def test_delete_student_not_found(self):
        url = '/delete_student'
        data = {
            'email': 'nonexistent@example.com'
        }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "no student found")
    
    def test_assign_student_teacher_success(self):
        Student.objects.create(email="student@example.com", name="Student Name", standard=10)
        Teacher.objects.create(email="teacher@example.com", name="Teacher Name", subject="Math")
        url = '/assign_student_teacher'
        data = {
            'student': 'student@example.com', 
            'teacher': 'teacher@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "relation created successfully")
    
    def test_assign_student_teacher_missing_input(self):
        url = '/assign_student_teacher'
        data ={
            'teacher': 'teacher@example.com'
        }
        response1 = self.client.post(url, data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response1.data['message'], "missing input")
        data = {
            'student': 'student@example.com'
        }
        response2 = self.client.post(url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.data['message'], "missing input")
        data = {
        }
        response3 = self.client.post(url, data, format='json')
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.data['message'], "missing input")

    def test_assign_student_teacher_student_not_found(self):
        Teacher.objects.create(email="teacher@example.com", name="Teacher Name", subject="Math")
        url = '/assign_student_teacher'
        data = {
            'student': 'nonexistent@student.com', 
            'teacher': 'teacher@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "student not found")

    def test_assign_student_teacher_student_not_found(self):
        Student.objects.create(email="student@example.com", name="Student Name", standard=10)
        url = '/assign_student_teacher'
        data = {
            'teacher': 'nonexistent@student.com', 
            'student': 'student@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "teacher not found")
