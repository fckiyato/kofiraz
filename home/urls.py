from django.urls import path
from . import views
#------------------------------

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('hotels/', views.HotelsView.as_view(), name='hotels'),
    path('hotelsdetail/<int:hotel_id>/', views.HotelsDetailView.as_view(), name='hotelsdetail_not_user'),
    path('hotelsdetail/<int:hotel_id>/<int:user_id>/', views.HotelsDetailView.as_view(), name='hotelsdetail'),
    path('room/<int:room_id>/', views.HotelRoomView.as_view(), name='hotelroom'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('agencyterms/', views.AgencyTermsView.as_view(), name='agencyterms'),
    path('aboutus/', views.AboutusView.as_view(), name='aboutus'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('faq/', views.faqView.as_view(), name='faq'),
    
]
