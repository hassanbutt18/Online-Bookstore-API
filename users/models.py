from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from users.managers import CustomUserManager

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50 )
    full_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    class Meta:
        unique_together = [['email', 'role']]
