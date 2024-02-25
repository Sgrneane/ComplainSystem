from django.shortcuts import render, HttpResponse,redirect,get_list_or_404, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage,EmailMultiAlternatives,send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django_otp.oath import totp
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model
from social_core.exceptions import AuthAlreadyAssociated

from . import decorators
from . import choices
from .models import CustomUser
from .forms import SignupForm, EditUserForm
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
                messages.error(request, 'Incorrect Username or Password!')
                return redirect('account:login_user')
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
        print('------hello------')
        role = request.POST.get('role')
        department = request.POST.get('department')
        
        if form.is_valid():            
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            phone = str(form.cleaned_data['phone_number'])
            password = form.cleaned_data['password']
            retype_password = form.cleaned_data['retype_password']
            
            if not handle_signup_validation(request, email, username, password, retype_password, phone):
                print('------erro------')
                return redirect('account:create_admin')
            
            
            form.cleaned_data.pop('retype_password')
            User = get_user_model()
            User.objects.create_user(
                role=role, 
                admin_category_id=department, 
                **form.cleaned_data
            )
            print('---created---')
            return redirect(reverse('main:all_user'))
        else:
            messages.error(request, 'User not created! Please fill the form with correct data!')
            print('----error2---')
    else:
        form = SignupForm()
    context = {'data': data}
    return render(request,'account/create_admin.html', context)


def edit_user(request,id):
    user = get_object_or_404(CustomUser, id=id)
    
    if request.user.id != user.id and request.user.role != 1:  #allows users to update their own details only while allowing admin to update other users details too
        messages.error(request, 'Cannot Access!')
        return redirect('user-edit', id=request.user.id)
    
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        
        email = request.POST.get("email")
        username = request.POST.get('username')

        if CustomUser.objects.exclude(id=user.id).filter(username=username).first():
            messages.info(request, f'User with this username "{username}" already exists')
            return redirect('main:my_account')
        
        if CustomUser.objects.exclude(id=user.id).filter(email=email).first():
            messages.info(request, f'User with this email "{email}" already exists')
            return redirect('main:my_account')
    
        if form.is_valid():
            form.save()
            if request.user.role == 1:
                messages.success(request, "User Details Updated Successfully")
                return redirect('main:my_account')
            else:
                messages.success(request, "Details Updated Successfully")
                return redirect('main:my_account')
        else:
            print(form.errors)
            messages.error(request, "Please fill the form with correct data")
    else:
        form = EditUserForm()
        
    context = {'user': user}
    return render(request, 'account/edit_user.html', context)


def change_password(request):
    user = get_object_or_404(CustomUser, id=request.user.id)
    
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('password')
        retype_new_password = request.POST.get('retype_password')
        
        if current_password == '' or new_password == '' or retype_new_password == '':
            messages.error(request, "Please fill all the fields")
            return redirect('account:change_password')
        
        if not user.check_password(current_password):
            messages.error(request, "Incorrect Current Password")
            return redirect('account:change_password')
            
        if new_password != retype_new_password:
            messages.error(request, "New Passwords didn't match")
            return redirect('account:change_password')
        
        if current_password == new_password:
            messages.error(request, "New Password should not be same as Current Password!")
            return redirect('account:change_password')
        
        user.set_password(new_password)
        user.save()
        #update_session_auth_hash(request, user_object) #user is not logged out after changing password
        messages.success(request, "Password Changed Successfully! Login with new password")
        return redirect('account:login_user')
        
    context = {'user': user}
    return render(request, 'account/change_password.html', context)

def admin_can_change_password(request,id):
    user_to_change_password = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        new_password = request.POST.get('password')
        retype_new_password = request.POST.get('retype_password')
        if new_password != retype_new_password:
            messages.error(request, "New Passwords didn't match")
            return redirect('account:admin_can_change_password',id=id)
        user_to_change_password.set_password(new_password)
        user_to_change_password.save()
        update_session_auth_hash(request, user_to_change_password)
        return redirect('main:all_user')
    context = {'user': user_to_change_password}
    return render(request, 'account/admin_can_change_password.html', context)

class CustomPasswordResetView(PasswordResetView):
    """
    Customizing the django default passwordresetview to check if users email exist in
    database before sending mail
    """
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        # Check if the email exists in the database
        if not CustomUser.objects.filter(email=email).exists():
            messages.error(self.request, "Email does not exist.")
            return self.form_invalid(form)
        return super().form_valid(form) 

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
