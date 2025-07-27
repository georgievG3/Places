from django.contrib import admin

from reservations.models import Reservation


# Register your models here.
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'check_in', 'check_out', 'guests', 'full_name', 'phone', 'created_at')
    list_filter = ('guests', 'created_at', 'check_in', 'check_out',)
    search_fields = ('listing__title', 'user',)
    ordering = ('-created_at',)
