from django.contrib import admin
from .models import Hotel,Room, HotelImage, RoomImage
#-------------------------------------
class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 10
    max_num = 10
#-------------------------------------
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'star', 'type')
    search_fields = ('name',)
    list_filter = ('star', 'type', 'offers_hotel',)
    
    fieldsets = (
        ('Hotel Informations', {'fields':('name', 'star', 'type', 'address', 'description', 'check_in_time', 'check_out_time', 'main_image', 'offers_hotel')}),
        ('Options', {'fields':('breakfast', 'wifi', 'swimming_pool', 'refrigerator', 'tea_maker', 'tv', 'air_condition', 'parking', 'turkish_hamam', 'pet', 'room_service')})
    )
    inlines = [HotelImageInline]
#-------------------------------------
class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 10
    max_num = 10
#-------------------------------------
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'hotel', 'price_per_night', 'agency_price', 'currency')
    search_fields = ('room_type', 'hotel_name')
    list_filter = ('hotel','room_type', 'offers_room')
    fieldsets =(
        ('Room Informations', {'fields':('hotel', 'room_type', 'price_per_night', 'agency_price', 'currency', 'image', 'description', 'offers_room')}),
    )
    inlines = [RoomImageInline]    
#-------------------------------------
admin.site.register(Hotel ,HotelAdmin)
admin.site.register(Room, RoomAdmin)