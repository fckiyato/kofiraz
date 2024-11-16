from django import forms
from .models import Booking, Passenger
from datetime import date
from django.core.exceptions import ValidationError
from datetime import timedelta

class BookingForm(forms.ModelForm):
    fullname = forms.CharField(
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
    passnum = forms.CharField(
        widget = forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'شماره پاسپورت',
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
        })
    )
    checkout = forms.DateField(
        widget = forms.DateInput(attrs={
            'class':'dropdown-item',
            'placeholder':'تاریخ خروج',
            'type': 'date',
        })
    )
    
    tax = forms.IntegerField(
        widget = forms.NumberInput(attrs={
            'class':'bookkng-pay-info',
        })
    )
    totalprice = forms.IntegerField(
        widget = forms.NumberInput(attrs={
            'class':'booking-pay-info'
        })
    )
    
    class Meta:
        model = Booking
        fields = [
            'fullname','passnum','burndate', 'adult', 'children', 'night',
            'checkin', 'checkout','tax', 'totalprice'
            ]
        
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
        model = Passenger
        fields = ['fullname', 'passport_number', 'birthdate']
#-----------------------------------------------------
class GuestFormSet(forms.BaseFormSet):
    def clean(self):
        
        if any(self.errors):
            return
        guest_count = len(self.forms)
        
        if guest_count == 0:
            raise forms.ValidationError("حداقل تعداد مسافر نمیتواند کمتر از یک نفر باشد")
        
        for form in self.forms:
            if not form.cleaned_data.get('fullname') or not form.cleaned_data.get('passport_number') or not form.cleaned_data.get('birthdate'):
                raise forms.ValidationError("همه فیلد ها باید تکمیل شوند.")
        return self.cleaned_data
