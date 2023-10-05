from django.shortcuts import render, HttpResponse,redirect,get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage,EmailMultiAlternatives,send_mail
from django.contrib.auth.hashers import make_password
from django_otp.oath import totp
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model
from social_core.exceptions import AuthAlreadyAssociated

from . import decorators
from . import choices
from .models import CustomUser
from .forms import SignupForm
from .validation import handle_signup_validation

from main.models import ComplainName


def signup(request):
    """For creating regular users."""
    if request.method=='POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            phone = str(form.cleaned_data['phone_number'])
            password = form.cleaned_data['password']
            retype_password = form.cleaned_data['retype_password']
            
            if not handle_signup_validation(request, email, username, password, retype_password, phone):
                return redirect('account:signup')
            
            form.cleaned_data.pop('retype_password')
            User = get_user_model()
            User.objects.create_user(**form.cleaned_data)
            return redirect(reverse('account:login_user'))
        else:
            messages.error(request, 'User not created! Please fill the form with correct data!')
    else:
        form = SignupForm()
    return render(request, 'account/signup.html')


@decorators.authentication_not_required  
def login_user(request):
    if(request.method=='POST'):
        email=request.POST['email']
        password=request.POST['password']
        try:
            user=authenticate(request,username=email, password=password)
            if user is not None:
                login(request,user)
                return redirect(reverse('main:dashboard'))
            else:
                return HttpResponse("Invalid Credentials")
        except AuthAlreadyAssociated:
            # Handle the case where the Google account is already associated with another account
            return redirect(reverse('main:dashboard'))
    else:
        return render(request,'account/login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect(reverse('main:index'))


def create_admin(request):
    """For creating users with deifferent roles and departments by superadmin."""
    data = {
        'role_choices' : choices.ROLE_CHOICES,
        'department_choices' : ComplainName.objects.all()
    }
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        role = request.POST.get('role')
        department = request.POST.get('department')
        
        if form.is_valid():            
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            phone = str(form.cleaned_data['phone_number'])
            password = form.cleaned_data['password']
            retype_password = form.cleaned_data['retype_password']
            
            if not handle_signup_validation(request, email, username, password, retype_password, phone):
                return redirect('account:create_admin')
            
            form.cleaned_data.pop('retype_password')
            User = get_user_model()
            User.objects.create_user(
                role=role, 
                admin_category_id=department, 
                **form.cleaned_data
            )
            return redirect(reverse('account:create_admin'))
        else:
            messages.error(request, 'User not created! Please fill the form with correct data!')
    else:
        form = SignupForm()
    context = {'data': data}
    return render(request,'account/create_admin.html', context)

def forget_password(request):
    if request.method=='POST':
        user_email=request.POST.get('user_email')
        subject="Hello Prasashan OTP alert!!"
        message=f"Please use given OTP to reset your password."
        msg = EmailMessage(subject,message, to=(user_email))
        msg.send()
        return HttpResponse("Email for OTP sent successfully.")

    return render(request,'account/forget-password.html')

# def generate_otp():
#     otp = ''.join(random.choices('0123456789', k=6))
#     return otp
    
# def otp_verify(request):
#     subject = 'Your OTP Code'
#     message = f'Your OTP code is:'
#     recipient_list = 

#     send_mail(subject, message,recipient_list)

def index(request):
    return render(request, 'account/create_admin.html')
