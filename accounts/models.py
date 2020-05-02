from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    GRADE = [
     ("1", "1"), 
    ("2", "2"), 
    ("3", "3"), 
    ("4", "4"), 
    ("5", "5"), 
    ("6", "6"), 
    ("7", "7"), 
    ("8", "8"), 
    ("9", "9"), 
    ("10", "10"), 
    ("11", "11"), 
    ("12", "12"), 
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #Class can be imported from Grade entity 
    grade = models.CharField( max_length=20, choices=GRADE,default='1')


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Specialty = models.CharField(max_length=200)
    