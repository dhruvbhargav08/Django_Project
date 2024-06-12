from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length = 50,default='',primary_key=True,null=False)
    name = models.CharField(max_length = 50,default='',null=False)
    password = models.CharField(max_length = 256,default='',null=False)