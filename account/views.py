from django.shortcuts import render, HttpResponse,redirect,get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage,EmailMultiAlternatives,send_mail
from django.contrib.auth.hashers import make_password
from django_otp.oath import totp
from django.contrib.auth.decorators import login_required,user_passes_test
from social_core.exceptions import AuthAlreadyAssociated
from django.contrib import messages
from django.urls import reverse
from . import decorators
from .models import CustomUser

# Create your views here.
def signup(request):
    if (request.method=='POST'):
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['user_email']
        password=make_password(request.POST['user_password'])
        phonenumber=request.POST['user_phonenumber']
        if CustomUser.objects.filter(email=email).first():
            messages.info(request, f'User with this email "{ email }" already exists')
            return redirect(reverse('account:signup'))
        if CustomUser.objects.filter(username=username).first():
            messages.info(request, f'User with this username "{ username }" already exists')
            return redirect('account:signup') 
        CustomUser.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone_number=phonenumber,
        )
        return redirect(reverse('account:login_user'))
    else:
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
    if (request.method=='POST'):
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('user_email')
        password=make_password(request.POST.get('user_password'))
        phonenumber=request.POST.get('user_phonenumber')
        user_role = int(request.POST.get('user_role', None))
        user_category=request.POST.get('user_category',None)
        user_data= {
            'first_name':first_name,
            'last_name':last_name,
            'email':email,
            'phone_number':phonenumber,
            'role':user_role,
            'admin_category':user_category,
            'email_verified': True,
        }
        if CustomUser.objects.filter(email=user_data['email']).first():
                messages.info(request, f'User with this email "{user_data["email"]}" already exists')
                return redirect('account:signup')
        if CustomUser.objects.filter(username=user_data['username']).first():
                messages.info(request, f'User with this username "{user_data["username"]}" already exists')
                return redirect('account:signup')
        CustomUser.objects.create(password=password, **user_data)
        print(user_role)
        return redirect(reverse('main:admin_dashboard'))
    else:

        return render(request,'account/create_admin.html')

def forget_password(request):
    if request.method=='POST':
        user_email=request.POST.get('user_email')
        subject="Hello Prasashan OTP alert!!"
        message=f"Please use given OTP to reset your password."
        msg = EmailMessage(subject,message, to=(user_email))
        msg.send()
        return HttpResponse("Email for OTP sent successfully.")

    return render(request,'account/forget-password.html')

def generate_otp():
    otp = ''.join(random.choices('0123456789', k=6))
    return otp
    
# def otp_verify(request):
#     subject = 'Your OTP Code'
#     message = f'Your OTP code is:'
#     recipient_list = 

#     send_mail(subject, message,recipient_list)


