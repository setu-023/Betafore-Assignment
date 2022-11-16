from django.db import models
from django.contrib.auth.models import AbstractUser

import random

class User(AbstractUser):

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)

    name = models.CharField(max_length=255, default='')
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, default='')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = (random.randint(1,999999))
            print(self.otp)
        super().save(*args, **kwargs)