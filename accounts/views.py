from django.contrib.auth import authenticate, login
from django.shortcuts import render,  redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import VerifyCodeForm, NormalRegisterForm, AgencyRegisterForm,UserLoginForm, CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib import messages
import random
from utils import send_otp_code
from .models import otpCode, User
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_view
from django.utils import timezone
#-----------------------------------------------------
#----------------Login/Register-----------------------
class LoginView(View):
    
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:home')
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {'form':form})
    
    
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(phone=phone)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(agency_owner_phone=phone)
                except User.DoesNotExist:
                    messages.error(request, 'کاربری با این مشخصات یافت نشد', 'error')
                    return redirect('accounts:login')
            if not user.is_active:
                if hasattr(user, 'agency_owner_phone') and user.agency_owner_phone == phone:
                    messages.error(request, 'حساب کاربری شما فعال نیست، لطفا با پشتیبانی تماس بگیرید', 'warning')
                else:
                    messages.error(request, 'حساب کاربری شما فعال نیست', 'warning')
                return redirect('accounts:login')
            user = authenticate(request, phone=user.phone, password=password)
            if user is not None:
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                login(request, user)
                messages.success(request, 'کاربر گرامی به کوفیراز خوش آمدید', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            else:
                messages.error(request, 'شماره تلفن همراه ویا رمز عبور خود را اصلاح فرمایید', 'danger')
                return redirect('accounts:login')    
        messages.error(request, 'لطفا دوباره امتحان کنید!', 'primary')
        return redirect('accounts:login')
#-----------------------------------------------------
class AgencyRegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:home')
        form = AgencyRegisterForm()
        return render(request, 'accounts/register_agency.html', {'form':form})
    
    def post(self, request):
        form = AgencyRegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.is_agency = True
            user.save()
            messages.success(request, 'کاربر گرامی حساب کاربری شما با موفقیت ایجاد شد ولی در حالت تعلیق قرار گرفته است.جهت احراز هویت مشخصات آژانس خود با پشتیبانی تماس حاصل فرمایید.', 'success')
            return redirect('home:home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return render(request, 'accounts/register_agency.html', {'form':form})
#-----------------------------------------------------
class NormalRegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:home')
        form = NormalRegisterForm()
        return render(request, 'accounts/register_normal.html', {'form': form})

    def post(self, request):
        form = NormalRegisterForm(request.POST)
        if form.is_valid():
            random_code = random.randint(100000, 999999)
            send_otp_code(form.cleaned_data['phone'], random_code)
            otpCode.objects.create(phone=form.cleaned_data['phone'], code=random_code)
            request.session['UserRegisterInfo'] = {
                'phone': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'fullname': form.cleaned_data['fullname'],
                'password': form.cleaned_data['password2'],
            }
            messages.success(request, 'کد یکبارمصرف به شماره تلفن ثبت شده ارسال گردید.', 'success')
            return redirect('accounts:verify_code')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return render(request, 'accounts/register_normal.html', {'form': form})
#-----------------------------------------------------
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home:home') 
#-----------------------------------------------------
#------------------Profile----------------------------
class ProfileView(LoginRequiredMixin ,View):
    def get(self, request):
        return render(request, 'accounts/profile.html')
    
    def post(self, request):
        pass
    
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)
#-----------------------------------------------------
class ProfileBookingView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/profilebooking.html')
#-----------------------------------------------------
class ProfileInfoView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.is_agency:
            context = {
                'agency_name': user.agency_name,
                'agency_owner_name': user.agency_owner_name,
                'agency_owner_phone': user.agency_owner_phone,
            }
        else:
            context = {
                'fullname': user.fullname,
                'email': user.email,
                'phone': user.phone,
            }
        return render(request, 'accounts/profileinfo.html', context)
#-----------------------------------------------------
class ProfileSettingView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.is_agency:
            context = {
                'agency_name':user.agency_name,
                'agency_owner_name':user.agency_owner_name,
                'agency_owner_phone':user.agency_owner_phone,
                'agency_email':user.agency_email
            }
        else:
            context ={
                'fullname':user.fullname,
                'email':user.email,
                'phone':user.phone
            }
        return render(request, 'accounts/profilesetting.html', context)
    
    def post(self, request):
        user = request.user
        
        # Check if user is an agency or normal user and handle the form submission accordingly
        if user.is_agency:
            # Get updated data from the form submission
            agency_name = user.agency_name
            agency_owner_name = request.POST.get('agency_owner_name')
            agency_owner_phone = user.agency_owner_phone  # This should remain unchanged
            agency_email = user.agency_email  # Read-only field
            
            # Update the agency user fields
            user.agency_name = agency_name
            user.agency_owner_name = agency_owner_name
            user.save(update_fields=['agency_owner_name',])
            
            messages.success(request, 'اطلاعات آژانس با موفقیت بروزرسانی شد', 'success')
        else:
            # For normal users, update the full name only (phone and email are read-only)
            fullname = request.POST.get('fullname')
            phone = user.phone  # Read-only field
            email = user.email  # Read-only field
            
            # Update the normal user fields
            user.fullname = fullname
            user.save(update_fields=['fullname'])
            
            messages.success(request, 'اطلاعات کاربری با موفقیت بروزرسانی شد', 'success')
        return redirect('accounts:profilesetting')
#-----------------------------------------------------
class UserRegisterVerifyCodeView(View):
    def get(self, request):
        form = VerifyCodeForm()
        return render(request, 'accounts/verify.html', {'form': form})
    
    def post(self, request):
        user_session = request.session.get('UserRegisterInfo')
        if not user_session:
            messages.error(request, 'ارتباط شما قطع شد. لطفا دوباره برای گرفت کدیکبارمصرف اقدام فرمایید', 'danger')
            return redirect('accounts:normal_register')

        phone = user_session['phone']
        code_instance = otpCode.objects.filter(phone=phone).order_by('-id')

        if code_instance.exists():
            code_instance = code_instance.first()

            form = VerifyCodeForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                if cd['code'] == code_instance.code:
                    user = User.objects.create_user(
                        user_session['phone'],
                        user_session['email'],
                        user_session['fullname'],
                        user_session['password']
                    )
                    user.is_active = True
                    user.save()
                    code_instance.delete()
                    messages.success(request, 'ثبت نام شما با موفقیت به پایان رسید', 'success')
                    return redirect('accounts:login')
                else:
                    messages.error(request, 'کد وارد شده صحیح نمیباشد', 'danger')
                    return redirect('accounts:verify_code')
            else:
                messages.error(request, 'اخطاریه های درج شده را اصلاح فرمایید', 'danger')
                return redirect('accounts:verify_code')
        else:
            messages.error(request, 'کد یکبارمصرفی برای این شماره تلفن یافت نشد', 'danger')
            return redirect('accounts:normal_register')
#-----------------------------------------------------
#----------------Password Reset-----------------------
class UserPasswordResetView(auth_view.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'
    form_class = CustomPasswordResetForm
#-----------------------------------------------------
class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'
#-----------------------------------------------------
class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
    form_class = CustomSetPasswordForm
#-----------------------------------------------------
class UserPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
#-----------------------------------------------------
#-----------------------------------------------------
