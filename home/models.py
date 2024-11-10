from django.db import models
from accounts.models import User
#--------------------------------------
class Hotel(models.Model):
    hotel_star = [
        (3, '3 Star'),
        (4, '4 Star'),
        (5, '5 Star'),
    ]
    
    hotel_type = [
        ('هتل', 'هتل'),
        ('سوئیت', 'سوئیت'),
    ]
    
    name = models.CharField(max_length=254, verbose_name='نام هتل')
    address = models.TextField(verbose_name='آدرس هتل')
    description = models.TextField(verbose_name='توضیحات تکمیلی', blank=True, null=True)
    star = models.IntegerField(choices=hotel_star, default=3, verbose_name='ستاره هتل')
    type = models.CharField(max_length=254, choices=hotel_type, default='هتل', verbose_name='نوع هتل')
    check_in_time = models.TimeField(verbose_name='ساعت تحویل اتاق')
    check_out_time = models.TimeField(verbose_name='ساعت تخلیه اتاق')
    main_image = models.ImageField(upload_to="hotels/main_images/" ,blank=True, null=True)
    offers_hotel = models.BooleanField(default=False, verbose_name='هتل پیشنهادی', blank=True, null=True)
    
    
    breakfast = models.BooleanField(default=False, verbose_name='وعده صبحانه')
    wifi = models.BooleanField(default=False, verbose_name='وای فای')
    swimming_pool = models.BooleanField(default=False, verbose_name='استخر شنا')
    refrigerator = models.BooleanField(default=False, verbose_name='یخچال')
    tea_maker = models.BooleanField(default=False, verbose_name='چای ساز')
    tv = models.BooleanField(default=False, verbose_name='تلویزیون')
    air_condition = models.BooleanField(default=False, verbose_name='کولرگازی')
    parking = models.BooleanField(default=False, verbose_name='پارکینگ اخنصاصی')
    turkish_hamam = models.BooleanField(default=False, verbose_name='حمام ترکی')
    pet = models.BooleanField(default=False, verbose_name='ورود حیوان خانگی')
    room_service = models.BooleanField(default=False, verbose_name='سرویس نظافت اتاق')
    
    def __str__(self):
        return f"Hotel -- {self.name} -- {self.star} star"
#-----------------------------------------------------
class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='HotelImages')
    image = models.ImageField(upload_to='hotels/images/', verbose_name='عکس های هتل')
    
    def __str__(self):
        return f"Images For {self.hotel.name}"
#-----------------------------------------------------    
class Room(models.Model):
    room_types = [
        ('اتاق ۱ تخته', 'Single Room'),
        ('اتاق ۲ تخته', 'Double Room'),
        ('اتاق ۳ تخته', 'Triple Room'),
        ('اتاق ۴ تخته', 'Quad Room'),
        ('اتاق ۵ تخته', 'Five Bed Room'),
        ('اتاق ۶ تخته', 'Six Bed Room'),
        ('اتاق ۷ تخته', 'Seven Bed Room'),
        ('اتاق ۸ تخته', 'Eight Bed Room'),
        ('اتاق ۹ تخته', 'Nine Bed Room'),
        ('اتاق ۱۰ تخته', 'Ten Bed Room'),
    ]
    
    currency_type = [
        ('TL', '₺'),
        ('euro', '€'),
    ]
    
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='Room')
    room_type = models.CharField(max_length=254, choices=room_types)
    price_per_night = models.IntegerField()
    agency_price = models.IntegerField(blank=True, null=True)
    currency = models.CharField(max_length=4, choices=currency_type, default='TL')
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='rooms/main_images/')
    offers_room = models.BooleanField(default=False, verbose_name='اتاق پیشنهادی',blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.room_type} -- from {self.hotel}"
#-----------------------------------------------------
class RoomImage(models.Model):
    hotel = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='RoomsImages')
    image = models.ImageField(upload_to='room/images/', verbose_name='عکس های اتاق ها')
    
    def __str__(self):
        return f"Images For {self.hotel.room_type}"
#-----------------------------------------------------
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    hotel_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_comment', blank=True, null=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_comment', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"-- User = {self.user} -- Commented={self.body[:30]}"
#-----------------------------------------------------