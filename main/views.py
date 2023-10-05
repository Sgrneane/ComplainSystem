from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import generics
from account.decorators import is_admin,is_superadmin,is_user
from django.contrib.auth.decorators import login_required,user_passes_test
from . models import Complain, ComplainName
from .forms import ComplainForm

# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def dashboard(request):
    return render(request,'main/dashboard.html')

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
        return redirect(reverse('main:my_complain'))
    
    context = {'complain_name':complain_name}

    return render(request, 'main/create-complain.html', context)

@login_required
def my_complain(request):
    user=request.user
    all_complains=user.my_complains.all()
    # print(all_complains)
    context={
        'all_complains':all_complains
    }
    return render(request,'main/mycomplain.html',context)

#Rendering all complains to admin panel
def view_complain(request):
    return render(request,'main/view_complain.html')


#View category Function
def view_category(request):
    categories=ComplainName.objects.all()
    context={
        'categories':categories
    }
    print(categories)
    return render(request,'main/view_category.html',context)

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

def all_complain(request):
    return render(request,'main/all_complains.html')

def anonymous_complain(request):
    return render(request,'main/anonymous_complains.html')

def all_user(request):
    return render(request, 'main/all_user.html')
def my_account(request):
    return render(request,'main/myaccount.html')



