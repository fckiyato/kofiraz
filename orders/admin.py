from django.contrib import admin
from .models import Booking, Passenger

class BookingAdmin(admin.ModelAdmin):
    list_display = ("fullname","is_paid")
    search_fields = ("fullname",)
    list_filter = ('is_paid',)
    
admin.site.register(Booking, BookingAdmin)


class PassengerAdmin(admin.ModelAdmin):
    list_display = ('booking', 'fullname', 'passport_number')
    search_fields = ('fullname', 'passport_number')
    list_filter = ('booking',)
    
admin.site.register(Passenger, PassengerAdmin)