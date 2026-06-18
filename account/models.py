from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField


def username_to_slug(value):
    return value.lower().replace(' ', '_')


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Account(BaseModel, AbstractUser):
    slug = AutoSlugField(populate_from='username', unique=True, slugify=username_to_slug)
    role = models.CharField(max_length=16, choices=[
        ('admin', 'Admin'),
        ('user', 'User'),
    ], default='user')

    def get_absolute_url(self):
        return reverse('account:account', kwargs={'slug': self.slug})

