from django.contrib import admin
from .forms import UserChangeForm, UserCreationForm, NormalRegisterForm, AgencyRegisterForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, otpCode
from django.contrib.auth.models import Group
#-------------------------------------------------------------------
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ('agency_name', 'fullname', 'email', 'phone', 'is_superuser', 'is_agency', 'is_active')
    list_filter = ('is_active', 'is_agency')
    
    fieldsets = (
        ('User informations', {'fields':('fullname', 'phone', 'email', 'password', 'agency_name', 'agency_owner_name', 'agency_owner_phone', 'agency_email')}),
        ('permissions', {'fields':('is_active', 'is_agency', 'is_superuser', 'last_login')}),
    )
    add_fieldsets = (
        (None, {'fields':('phone', 'email', 'fullname', 'agency_name', 'agency_owner_name', 'agency_owner_phone', 'password1', 'password2')}),
    )
    search_fields = ('email', 'fullname')
    ordering = ('fullname',)
    filter_horizontal = ()
    
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
#-------------------------------------------------------------------
admin.site.register(otpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code', 'created')
#-------------------------------------------------------------------