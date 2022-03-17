from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    user_type=models.CharField(max_length=30,choices=(('1','Admin'),('2','Teacher'),('3','Student')))
    mobile_number=models.CharField(max_length=12)
    address=models.TextField(max_length=400)
    def __str__(self):
        return self.username

