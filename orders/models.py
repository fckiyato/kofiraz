from django.db import models
from accounts.models import User
from home.models import Room, Hotel
from django.utils import timezone
from datetime import timedelta
#-----------------------------------------------------
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    
    checkin = models.DateField()
    checkout = models.DateField()
    
    fullname = models.CharField(max_length=50)
    passnum = models.CharField(max_length=9, unique=True)
    burndate = models.DateField()

    adult = models.PositiveIntegerField()
    children = models.PositiveIntegerField()
    night = models.PositiveIntegerField()
    tax = models.PositiveIntegerField(default=10)
    PAYMENT_METHOD_CHOICES = [
        ('card_to_card','کارت به کارت'),
        ('cash','نقدی'),
    ]
    payment_method = models.CharField(max_length=13, choices=PAYMENT_METHOD_CHOICES, default="cart_to_cart", verbose_name="روش پرداخت ", blank=True)
    totalprice = models.IntegerField(blank=True, null=True)
    mustpay = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    
        
    def save(self, *args, **kwargs):
        self.checkout = self.checkin + timedelta(days=self.night)
        room_price_per_night = self.room.price_per_night
        self.totalprice = (room_price_per_night * self.night) + self.tax
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Booking {self.id} for {self.fullname}"
    
    class Meta:
        ordering = ['-checkin']
#-----------------------------------------------------
class Passenger(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=9)
    birthdate = models.DateField()
    
    def __str__(self):
        return f"Guest: {self.fullname} - Passport Number: {self.passport_number}"
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