from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class User(AbstractUser):
    Role=(
        ('teacher','teacher'),
        ('admin','admin'),
        ('student','student')
    )
    role=models.CharField(max_length=10,choices=Role,default='student')


    def __str__(self):
        return f"{self.username} {self.role}"
    


class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username
    
class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
