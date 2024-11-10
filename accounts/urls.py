from django.urls import path
from . import views
#----------------------------------
app_name = 'accounts'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/',views.LogoutView.as_view(), name='logout'),
    path('agencyregister/', views.AgencyRegisterView.as_view(), name='agency_register'),
    path('normalregister/', views.NormalRegisterView.as_view(), name='normal_register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/booking/', views.ProfileBookingView.as_view(), name='profilebooking'),
    path('profile/info/', views.ProfileInfoView.as_view(), name='profileinfo'),
    path('profile/setting/', views.ProfileSettingView.as_view(), name='profilesetting'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'), 
]