from django.db import models

from accounts.models import AppUser


# Create your models here.
class Location(models.Model):
    TERRAIN_CHOICES = [
        ('sea', 'Море'),
        ('mountain', 'Планина'),
        ('lake', 'Езеро'),
        ('city', 'Град'),
        ('village', 'Село'),
        ('other', 'Друг'),
    ]
    region = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    terrain_type = models.CharField(max_length=20, choices=TERRAIN_CHOICES, default='other')


class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Camping(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Listing(models.Model):
    LISTING_TYPE_CHOICES = [
        ('camper', 'Каравана'),
        ('bungalow', 'Бунгало'),
        ('apartment', 'Апартамент'),
    ]

    title = models.CharField(max_length=100)
    mini_description = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    camping = models.ForeignKey(Camping, on_delete=models.SET_NULL, null=True, blank=True)
    rooms = models.PositiveIntegerField(null=True, blank=True)
    pets_allowed = models.BooleanField(default=False)
    min_nights = models.PositiveIntegerField(default=1)
    max_people = models.PositiveIntegerField(default=1)
    square_meters = models.PositiveIntegerField(null=True, blank=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    description = models.TextField()
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='listings')


class Image(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listing_images/')



