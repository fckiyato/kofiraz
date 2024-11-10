from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
#-----------------------------------------------------------
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تایید رمز عبور', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('fullname', 'email', 'phone', 'agency_name', 'agency_owner_name', 'agency_owner_phone')
        
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("رمز عبور ها یکسان نیستند")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
#-----------------------------------------------------------
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label = 'password')
    class Meta:
        model = User
        fields = ('fullname', 'phone', 'fullname', 'password', 'last_login', 'is_agency', 'agency_name', 'agency_owner_name', 'agency_owner_phone')
        
    def clean_password(self):
        return self.initial["password"]
#-----------------------------------------------------------
class AgencyRegisterForm(forms.ModelForm):
    
    agency_name = forms.CharField(
        max_length=254,  
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'نام آژانس'
        })
    )
    agency_owner_name = forms.CharField(
        max_length=254,  
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'نام مدیر آژانس'
        })
    )
    agency_owner_phone = forms.CharField(
        max_length=11,  
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'تلفن همراه مدیر آژانس'
        })
    ) 
    agency_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'آدرس ایمیل آژانس'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'رمز عبور',
        })
    )
    password2 = forms.CharField( 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'تکرار رمز عبور'
        })
    )

    class Meta:
        model = User
        fields = ['agency_name', 'agency_owner_name', 'agency_owner_phone', 'agency_email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('رمز عبور و تکرار آن یکسان نمیباشد')
        return password2
    
    def clean_agency_name(self):
        agency_name = self.cleaned_data.get('agency_name')
        user = User.objects.filter(agency_name = agency_name).exists()
        if user:
            raise ValidationError('کاربر آژانسی با این نام آژانس قبلا ثبت نام کرده است')
        return agency_name
    
    def clean_agency_owner_phone(self):
        agency_owner_phone = self.cleaned_data.get('agency_owner_phone')
        user = User.objects.filter(agency_owner_phone = agency_owner_phone).exists()
        if user:
            raise ValidationError('مدیر آژانسی قبلا با این شماره تلفن ثبت نام کرده است')
        return agency_owner_phone
        
    def clean_agency_email(self):
        email = self.cleaned_data.get('agency_email')
        user = User.objects.filter(agency_email=email).exists()
        if user:
            raise ValidationError('آژانسی با این آدرس ایمیل قبلا ثبت نام کرده است')
        return email
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_agency = True
        user.is_active = False
        if commit:
            user.save()
        return user
#-----------------------------------------------------------
class NormalRegisterForm(forms.ModelForm):
    fullname = forms.CharField(
        max_length = 254,
        widget = forms.TextInput(attrs = {
            'class':'form-control',
            'placeholder':'نام و نام خانوادگی'
        })
    )
    email = forms.EmailField(
        widget = forms.TextInput(attrs = {
            'class':'form-control',
            'placeholder':'آدرس ایمیل',
        })
    )
    phone = forms.CharField(
        max_length=11,
        widget = forms.TextInput(attrs = {
            'class':'form-control',
            'placeholder':'شماره تلفن همراه',
            'autocomplete':'off',
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'رمز عبور',
            'autocomplete':'new-password',
        })
    )
    password2 = forms.CharField( 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'تکرار رمز عبور'
        })
    )
    
    class Meta:
        model = User
        fields = ['fullname', 'email', 'phone',]
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('رمز عبور و تکرار آن یکسان نمیباشد')
        return password2
        
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('کاربر گرامی ایمیل نامعتبر می باشد لطفا آدرس ایمیل دیگری را وارد کنید')
        return email
    
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        user = User.objects.filter(phone=phone).exists()
        if user:
            raise ValidationError('کاربر گرامی شماره تلفن نامعتبر می باشد لطفا با شماره تلفن دیگری ثبت نام کنید ')
        return phone
    
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        user.is_agency = False
        if commit:
            user.save()
        return user
#-----------------------------------------------------------
class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'کد یکبار مصرف'
        })
    )

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not str(code).isdigit():
            raise forms.ValidationError('کد یکبار مصرف باید عدد باشد')
        return code
#-----------------------------------------------------------
class UserLoginForm(forms.Form):
    phone = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' شماره تلفن همراه',
            'autocomplete': 'off',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور',
            'autocomplete': 'new-password',
        })
    )
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        # Check if the phone number is exactly 11 digits and consists only of numbers
        if not phone.isdigit() or len(phone) != 11:
            raise ValidationError('شماره تلفن همراه باید 11 رقم باشد و فقط شامل اعداد باشد.')

        return phone

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        password = cleaned_data.get('password')

        # Check if the phone number exists in either normal users or agency users
        try:
            user = User.objects.get(phone=phone)  # Check for normal user
        except User.DoesNotExist:
            try:
                user = User.objects.get(agency_owner_phone=phone)  # Check for agency user
            except User.DoesNotExist:
                raise ValidationError('کاربری با این مشخصات یافت نشد')

        # Optionally: You can add further checks on the user object, like is_active
        if user.is_active is False:
            raise ValidationError('حساب شما فعال نیست، لطفا با پشتیبانی تماس بگیرید.')

        return cleaned_data
#-----------------------------------------------------------
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="ایمیل",
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'ایمیل خود را وارد کنید'})
    )
#-----------------------------------------------------------
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("رمز عبور جدید"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور جدید را وارد کنید'}),
    )
    new_password2 = forms.CharField(
        label=_("تأیید رمز عبور جدید"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور جدید را دوباره وارد کنید'}),
    )
#-----------------------------------------------------------