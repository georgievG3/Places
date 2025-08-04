from django.contrib import admin

from listings.models import Listing, Amenity


# Register your models here.
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'owner', 'created_at', 'is_approved')
    list_filter = ('type', 'created_at')
    search_fields = ('title', 'description', 'mini_description')
    ordering = ('-created_at',)
    list_editable = ('is_approved',)

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
