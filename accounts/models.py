from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
#-----------------------------------------------------
class User(AbstractBaseUser):
    fullname = models.CharField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    
    agency_name = models.CharField(max_length=254, unique=True, blank=True, null=True)
    agency_owner_name = models.CharField(max_length=254, blank=True, null=True)
    agency_owner_phone = models.CharField(max_length=11, unique=True, blank=True, null=True)
    agency_email = models.EmailField(unique=True, blank=True, null=True)
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_agency = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'fullname']
    
    def __str__(self):
        return self.email or self.agency_name or self.agency_owner_phone
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser
    
    @property
    def staff_status(self):
        return self.is_staff
#-----------------------------------------------------
class otpCode(models.Model):
    phone = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.phone} -- {self.code} -- {self.created}"
#-----------------------------------------------------
