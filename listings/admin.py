from django.contrib import admin

from listings.models import Listing


# Register your models here.
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'owner', 'created_at', 'is_approved')
    list_filter = ('type', 'created_at')
    search_fields = ('title', 'description', 'mini_description')
    ordering = ('-created_at',)
    list_editable = ('is_approved',)