from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class myuser(AbstractUser):
    first_name = models.CharField(max_length = 30)
    email = models.EmailField(max_length = 70, unique = True)
    profile_pic = models.ImageField(default = 'default.png')

