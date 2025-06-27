from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class BaseUser(AbstractUser):
    rating = models.FloatField(default=0)