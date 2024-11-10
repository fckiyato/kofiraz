from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from .models import Hotel, Room
from accounts.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
#------------------------------------
class HomeView(View):
    def get(self, request):
        offered_hotels = Hotel.objects.filter(offers_hotel=True)
        offered_rooms = Room.objects.filter(offers_room = True)
        return render(request, 'home/home.html', {'offered_hotels':offered_hotels, 'offered_rooms':offered_rooms})
#------------------------------------
class HotelsView(View):
    def get(self, request):
        hotels = Hotel.objects.all()
        
        paginator = Paginator(hotels, 6)  # Show 3 hotels per page
        page = request.GET.get('page')  # Get current page number from request

        try:
            hotels = paginator.page(page)
        except PageNotAnInteger:
            hotels = paginator.page(1)  # If page is not an integer, deliver first page.
        except EmptyPage:
            hotels = paginator.page(paginator.num_pages) 
        
        return render(request, 'home/hotels.html', {'hotels':hotels})
#------------------------------------
class HotelsDetailView(View):
    def get(self, request, hotel_id, user_id=None):
        hotel = get_object_or_404(Hotel, id=hotel_id)
        rooms = Room.objects.filter(hotel=hotel)
        user = None
        if user_id is not None:
            user = get_object_or_404(User, id=user_id)
            
        context = {
            'hotel': hotel,
            'rooms': rooms,
            'user': user,
        }
        return render(request, 'home/hotelsdetail.html', context)
#------------------------------------
class HotelRoomView(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        hotel = room.hotel
        context = {
            'room': room,
            'hotel':hotel,
        }
        return render(request, 'home/hotelroom.html', context)
    
    
    def post(self, reqeust, *args, **kwargs):
        if reqeust.user.is_suthenticated:
            return redirect(reverse_lazy("orders:cart"))
        else:
            messages.error(reqeust, 'please login to complete your order!')
            return redirect(reverse_lazy("accounts:login"))
#------------------------------------
class TermsView(View):
    def get(self, request):
        return render(request, 'home/terms.html')
#------------------------------------
class AgencyTermsView(View):
    def get(self, request):
        return render(request, 'home/agencyterms.html')
#------------------------------------
class AboutusView(View):
    def get(self, request):
        return render(request, 'home/about.html')
#------------------------------------
class ContactView(View):
    def get(self, request):
        return render(request, 'home/contact.html')
#------------------------------------
class faqView(View):
    def get(self, reqeust):
        return render(reqeust, 'home/faq.html')
#------------------------------------