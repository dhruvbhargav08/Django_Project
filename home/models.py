from django.db import models

# Create your models here.
class Student(models.Model):
    email = models.CharField(max_length = 32,default='',primary_key=True,null=False)
    name = models.CharField(max_length = 16,default='',null=False)
    password = models.CharField(max_length = 256,default='',null=False)
    standard = models.IntegerField(default=0,null=False)

class Teacher(models.Model):
    email = models.CharField(max_length = 32,default='',primary_key=True,null=False)
    name = models.CharField(max_length = 16,default='',null=False)
    password = models.CharField(max_length = 256,default='',null=False)
    subject = models.CharField(max_length=16,default='',null=False)

class Student_Teacher_Relation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


