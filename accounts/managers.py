from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone, email, fullname, password=None):
        if not phone:
            raise ValueError('user must have phone number')
        
        if not email:
            raise ValueError('user must have email address')
        
        if not fullname:
            raise ValueError('user must have fullname')
        
        user = self.model(
            phone=phone, 
            email=self.normalize_email(email), 
            fullname=fullname,
            agency_name=None,
            agency_owner_name=None,
            agency_owner_phone=None,
            is_agency=False
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, phone, email, fullname, password=None):
        user = self.create_user(phone=phone, email=email, fullname=fullname, password=password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
    
    def create_agency_user(self, phone, email, fullname, agency_name, agency_owner_name, agency_owner_phone, password=None):
        if not agency_name:
            raise ValueError('Agency users must have an agency name')
        
        if not agency_owner_name:
            raise ValueError('Agency users must have an agency owner name')
        
        if not agency_owner_phone:
            raise ValueError('Agency users must have an agency owner phone')
        
        user = self.model(
            phone = phone,
            email = self.normalize_email(email),
            fullname = fullname,
            agency_name = agency_name,
            agency_owner_name = agency_owner_name,
            agency_owner_phone = agency_owner_phone,
        )
        user.is_agency = True
        user.set_password(password)
        user.save(using=self._db)
        return user  