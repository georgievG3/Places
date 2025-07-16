from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from listings.models import Listing


# Create your models here.
class Reservation(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.listing.title} ({self.check_in} до {self.check_out})"
