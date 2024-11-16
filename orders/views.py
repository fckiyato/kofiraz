from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Room, Hotel
from accounts.models import User
from .forms import BookingForm
from django.forms import modelformset_factory
from .models import Booking, Passenger
from .forms import BookingForm
#-------------------------------------------------------------------------
class BookingView(LoginRequiredMixin ,View):
    def get(self, request, user_id, room_id, hotel_id, **kwargs):
        form = BookingForm()
        room = get_object_or_404(Room, id=room_id)
        user = get_object_or_404(User, id=user_id)
        hotel = get_object_or_404(Hotel, id=hotel_id)
        
        
        content = {
            'room': room,
            'user': user,
            'hotel': hotel,
            'form': form,
            **kwargs
        }
        return render(request, 'orders/booking.html', content)
    
    
    def post(self, request, user_id, room_id, hotel_id):
        form = BookingForm(request.POST)
        room = get_object_or_404(Room, id=room_id)
        user = get_object_or_404(User, id=user_id)
        hotel = get_object_or_404(Hotel, id=hotel_id)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = user
            booking.hotel = hotel
            
            payment_method = request.POST.get('payment_method')
            booking.payment_method = payment_method
            
            booking.save()
            
            total_guests = int(request.POST.get('total_guests', 0))
            
            for i in range(1, total_guests + 1):
                passfullname = request.POST.get(f'passfullname_{i}')
                passnum = request.POST.get(f'passnum_{i}')
                burndate = request.POST.get(f'burndate_{i}')

                if passfullname and passnum and burndate:
                    guest = Passenger(
                        booking=booking,
                        fullname=passfullname,
                        passnum=passnum,
                        burndate=burndate,
                    )
                    guest.save()

            return redirect(reverse_lazy('success_url'))

        content = {
            'room': room,
            'user': user,
            'hotel': hotel,
            'form': form,
        }
        return render(request, 'orders/booking.html', content)
#-------------------------------------------------------------------------    
class BookingCompleteView(LoginRequiredMixin ,View):
    def get(self, reqeust):
        return render(reqeust, 'orders/booking_complete.html')
            
    
