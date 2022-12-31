from django.db import models

# Create your models here.
class users(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=200)
    email=models.EmailField()
    state=models.BooleanField()