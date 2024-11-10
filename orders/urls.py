from django.urls import path
from . import views


app_name  = 'orders'
urlpatterns = [
    path('booking/<int:user_id>/<int:room_id>/<int:hotel_id>/', views.BookingView.as_view(), name='booking'),
    path('bookingcomplete/', views.BookingCompleteView.as_view(), name='booking_complete'),
]
