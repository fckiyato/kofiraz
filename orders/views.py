from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Room, Hotel
from accounts.models import User
from .forms import BookingForm
from django.views.generic.edit import FormView
from django.forms import modelformset_factory
from .models import Booking, Guest
from .forms import BookingForm, GuestForm
#-------------------------------------------------------------------------
class BookingView(LoginRequiredMixin ,View):
    def get(self, request, user_id, room_id, hotel_id):
        form = BookingForm()
        room = get_object_or_404(Room, id=room_id)
        user = get_object_or_404(User, id=user_id)
        hotel = get_object_or_404(Hotel, id=hotel_id)
        
        GuestFormSet = modelformset_factory(Guest, form=GuestForm, extra=10)
        guest_formset = GuestFormSet(queryset=Guest.objects.none())
        
        
        content = {
            'room': room,
            'user': user,
            'hotel': hotel,
            'form': form,
            'guest_formset': guest_formset,
        }
        return render(request, 'orders/booking.html', content)
    
    
    def post(self, request, user_id, room_id, hotel_id):
        form = BookingForm(request.POST)
        room = get_object_or_404(Room, id=room_id)
        user = get_object_or_404(User, id=user_id)
        hotel = get_object_or_404(Hotel, id=hotel_id)

        GuestFormSet = modelformset_factory(Guest, form=GuestForm, extra=10)
        guest_formset = GuestFormSet(request.POST)

        if form.is_valid() and guest_formset.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = user
            booking.hotel = hotel
            booking.save()
            
            for guest_form in guest_formset:
                guest = guest_form.save(commit=False)
                guest.booking = booking
                guest.save()
            return redirect(reverse_lazy('success_url'))
        else:
            content = {
                'room': room,
                'user': user,
                'hotel': hotel,
                'form': form,
                'guest_formset': guest_formset,
            }
            return render(request, 'orders/booking.html', content)
#-------------------------------------------------------------------------    
class BookingCompleteView(LoginRequiredMixin ,View):
    def get(self, reqeust):
        return render(reqeust, 'orders/booking_complete.html')
            
    
