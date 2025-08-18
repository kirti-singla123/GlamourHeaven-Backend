from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service', 'date', 'time', 'created_at')
    search_fields = ('name', 'phone', 'service')
    list_filter = ('service', 'date')
