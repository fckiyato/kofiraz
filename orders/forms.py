from django import forms
from .models import Booking, Guest
from datetime import date
from django.core.exceptions import ValidationError
from datetime import timedelta

class BookingForm(forms.ModelForm):
    
    
    agency = forms.CharField(
        max_length = 50,
        widget = forms.TextInput(attrs = {
            'class':'form-control',
            'placeholder':'نام آژانس'
        })
    )
    passfullname = forms.CharField(
        widget= forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام و نام خانوادگی'
        })
    )
    burndate = forms.DateField(
        widget = forms.DateInput(attrs ={
            'class':'form-control',
            'placeholder':'تارییخ تولد به میلادی',
            'autocomplete':'off',
            'type':'date',
        }, format="%Y/%m/%d")
    )
    natid = forms.IntegerField(
        widget = forms.NumberInput(attrs = {
            'class':'form-control',
            'placeholder':'شماره کد ملی',
            'autocomplete':'off',
        })
    )
    passnum = forms.CharField(
        widget = forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'شماره پاسپورت',
            'autocomplete':'off',
        })
    )
    emailaddr = forms.EmailField(
        widget = forms.EmailInput(attrs={
            'class':'form-control',
            'placeholder':'آدرس ایمیل'
        })
    )
    phonenum = forms.CharField(
        max_length=11,
        widget = forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'شماره تلفن همراه',
            'autocomplete':'off',
        })
    )
    
    adult = forms.IntegerField(
        widget = forms.NumberInput(attrs={
            'class':'dropdown-item',
            'placeholder':'بزرگسالان',
        })
    )
    children = forms.IntegerField(
        widget = forms.NumberInput(attrs={
            'class':'dropdown-item',
            'placeholder':'کودکان',
        })
    )
    night = forms.IntegerField(
        widget = forms.NumberInput(attrs={
            'class':'dropdown-item',
            'placeholder':'تعداد شب'
        })
    )
    
    checkin = forms.DateField(
        widget = forms.DateInput(attrs={
            'class':'dropdown-item',
            'placeholder':'تاریخ ورود',
            'type': 'date',
        },format="%Y/%m/%d")
    )
    checkout = forms.DateField(
        widget = forms.DateInput(attrs={
            'class':'dropdown-item',
            'placeholder':'تاریخ خروج',
            'type': 'date'
        },format="%Y/%m/%d")
    )
    
    tax = forms.IntegerField(
        widget = forms.NumberInput(attrs={
            'class':'bookkng-pay-info',
        })
    )
    sumprice = forms.IntegerField(
        widget = forms.NumberInput(attrs={
            'class':'booking-pay-info'
        })
    )
    
    class Meta:
        model = Booking
        fields = ['agency', 'passfullname', 'natid', 'emailaddr', 'phonenum',
                  'passnum','burndate', 'adult', 'children', 'night',
                  'tax', 'checkin', 'checkout']
        
    def clean_checkin(self):
        checkin = self.cleaned_data.get("checkin")
        if checkin < date.today():
            raise ValidationError("تاریخ ورود نمی‌تواند در گذشته باشد")
        return checkin
    
    def clean(self):
        cleaned_data = super().clean()
        checkin = cleaned_data.get("checkin")
        night = cleaned_data.get("night")

        if night <= 0:
            self.add_error("night", "تعداد شب‌ها باید بیشتر از صفر باشد")

        if checkin and night:
            expected_checkout = checkin + timedelta(days=night)
            if "checkout" in cleaned_data:
                checkout = cleaned_data["checkout"]
                if checkout != expected_checkout:
                    self.add_error("checkout", "تاریخ خروج باید مطابق تعداد شب‌های رزرو باشد")

        adult = cleaned_data.get("adult")
        children = cleaned_data.get("children")
        if adult < 1:
            self.add_error("adult", "باید حداقل یک بزرگسال باشد")
        if adult > 10 or children > 10:
            raise ValidationError("تعداد مسافران نمی‌تواند بیشتر از 10 باشد")
        
        return cleaned_data    
#-----------------------------------------------------
class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['fullname', 'passport_number', 'birthdate']
#-----------------------------------------------------
class GuestFormSet(forms.BaseFormSet):
    def clean(self):
        
        if any(self.errors):
            return
        guest_count = len(self.forms)
        
        if guest_count == 0:
            raise forms.ValidationError("At least one guest is required.")
        max_guests = 10
        if guest_count > max_guests:
            raise forms.ValidationError(f"Cannot add more than {max_guests} guests.")
        
        for form in self.forms:
            if not form.cleaned_data.get('fullname') or not form.cleaned_data.get('passport_number') or not form.cleaned_data.get('birthdate'):
                raise forms.ValidationError("All fields for each guest must be filled out.")
        return self.cleaned_data
