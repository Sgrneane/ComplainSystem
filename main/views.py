from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from account.models import CustomUser
from account.decorators import is_admin,is_superadmin,is_user
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from . models import Complain, ComplainName, Response
from django.db.models import Count
from .forms import ComplainForm

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return dashboard(request)
    return render(request, 'main/index.html')

@login_required
def dashboard(request):
    return render(request,'main/dashboard.html')
#View category Function
@is_superadmin
def view_category(request):
    categories=ComplainName.objects.all()
    context={
        'categories':categories
    }
    return render(request,'main/view_category.html',context)
# View to add new Complain Category
@is_superadmin
def add_category(request):
    if request.method=="POST":
        complain_department=request.POST.get('complain_department')
        complain_category=request.POST.get('complain_category')
        ComplainName.objects.create(
            department_name=complain_department,
            complain_name=complain_category,

        )
        return redirect(reverse('main:view_category'))
    return render(request,'main/add_category.html')


@is_user
def create_complain(request):
    """For creating complains."""
    complain_name = ComplainName.objects.all()
    if request.method == 'POST':
        form = ComplainForm(request.POST, request.FILES)
        if form.is_valid():
            complain = form.save(commit=False)
            complain.created_by = request.user
            complain.save()
            return redirect(reverse('main:all_complains'))
        else:
            messages.info(request, f'Please select Complain Category')
            return redirect(reverse('main:create_complain'))
    
    context = {'complain_name':complain_name}

    return render(request, 'main/create-complain.html', context)


#viewing individual Complain
def view_complain(request, id):
    complain=get_object_or_404(Complain, id=id)
    context={
        'complain':complain
    }
    if request.method=="POST":
        response_body=request.POST.get("response_body")
        response_image = request.FILES.get("response_image")
        Response.objects.create(
            response_by=request.user,
            response_to_id=complain.id,
            response_body=response_body,
            response_image=response_image,
        )
        return redirect("main:view_complain", id=complain.id)
    return render(request,'main/view_complain.html',context)


#view for all complains for admin and superadmin
def all_complain(request):
    user=request.user
    search_title = request.GET.get('search_title', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    reset_button = request.GET.get('reset_button', '')
    if user.role == 1:
        complains=Complain.objects.filter(
            created_by__isnull= False
        ).annotate(response_count = Count('response'))
        complains = complains.filter(response_count = 0)

    elif user.role == 2:
        complains=Complain.objects.filter(
            Q(to_complain__department_name = user.admin_category.department_name) & 
            Q(created_by__isnull= False)
        ).annotate(response_count = Count('response'))
        complains = complains.filter(response_count = 0)
    else:
        my_complains=Complain.objects.filter(created_by=user).annotate(response_count=Count('response'))
        complains=my_complains.filter(response_count=0)
    if reset_button:
        pass
    else:
        if search_title:
            complains = complains.filter(
                Q(complain_title__icontains=search_title) |
                Q(complain_message__icontains=search_title)
            )
        if from_date:
            complains = complains.filter(created_date__gte=from_date)
        if to_date:
            complains = complains.filter(created_date__lte=to_date)
    context={
        'complains' :complains,
    }
    return render(request,'main/all_complains.html',context)



# Complain_responses
def complain_responses(request):
    user=request.user
    if user.role == 1:
        responses=Response.objects.all()
    elif user.role == 2:
        responses=user.responses.all()
    else:
        my_complains=user.my_complains.all()
        responses=Response.objects.filter(response_to__in=my_complains)
    context={
        'responses': responses
    }
    return render(request, 'main/responses.html', context)

def view_response(request, id):
    complain=get_object_or_404(Complain, id=id)
    context={
        'complain':complain
    }
    return render(request,'main/view_response.html',context)


@is_superadmin
def all_user(request):
    users=CustomUser.objects.all()
    context={
        'users':users,
    }
    return render(request, 'main/all_user.html',context)
@is_superadmin
def view_user(request,id):
    user=get_object_or_404(CustomUser, id=id)
    context={
        'user':user,
    }
    return render(request,'main/view_user.html',context)

def my_account(request):
    return render(request,'main/myaccount.html')


#Anonymous Complain /limiting anonymous user to have maximum of 2 complains
def anonymous_form(request):
    complain_name = ComplainName.objects.all()
    context = {'complain_name':complain_name}
    complaints_today = request.session.get('complaints_today', [])
    if len(complaints_today) >= 2:
        return redirect(reverse('main:index'))
    if request.method == 'POST':
        form = ComplainForm(request.POST, request.FILES)
        if form.is_valid():
            complain = form.save(commit=False)
            complain.save()
            current_date_str = datetime.now().date().isoformat()
            complaints_today.append(current_date_str)
            request.session['complaints_today'] = complaints_today
            request.session.save() 
        return redirect(reverse('main:index'))
    return render(request,'main/anonymous_form.html',context)

#views for anonymous Complains
def anonymous_complain(request):
    user=request.user
    if user.role == 1:
        anonymous_complains=Complain.objects.filter(created_by__isnull= True)
    context={
        'anonymous_complains':anonymous_complains
    }
    return render(request,'main/anonymous_complains.html',context)

#View for responding to the complain

def AboutUs(request):
    context={}
    return render(request,'main/aboutus.html',context)


def privacy(request):
    context={}
    return render(request,'main/privacy.html')

def faq(request):
    return render(request,'main/FAQ.html')

