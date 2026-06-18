from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Account(BaseModel, AbstractUser):
    role = models.CharField(max_length=16, choices=[
        ('admin', 'Admin'), 
        ('user', 'User')
    ], default='user')
    