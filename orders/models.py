from django.db import models
from accounts.models import User
from home.models import Room, Hotel
from django.utils import timezone
from datetime import timedelta
#-----------------------------------------------------
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    
    fullname = models.CharField(max_length=50)
    natid = models.IntegerField(unique=True)
    passnum = models.CharField(max_length=9, unique=True)
    phonenum = models.CharField(max_length=11 ,unique=True)
    burndate = models.DateField()
    

    adult = models.PositiveIntegerField()
    children = models.PositiveIntegerField()
    night = models.PositiveIntegerField()
    tax = models.PositiveIntegerField(default=10)
    
    checkin = models.DateField()
    checkout = models.DateField()
    
    
    def save(self, *args, **kwargs):
        self.checkout = self.checkin + timedelta(days=self.night)
        room_price_per_night = self.room.price_per_night
        self.sumprice = (room_price_per_night * self.night) + self.tax
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Booking {self.id} for {self.user.fullname}"
    
    class Meta:
        ordering = ['-checkin']
#-----------------------------------------------------
class Guest(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=11)
    birthdate = models.DateField()
    
    def __str__(self):
        return self.fullname
#-----------------------------------------------------
class BookingComplete(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.fullname}"
#-----------------------------------------------------