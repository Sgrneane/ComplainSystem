from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
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

#View category Function
def view_category(request):
    categories=ComplainName.objects.all()
    context={
        'categories':categories
    }
    print(categories)
    return render(request,'main/view_category.html',context)
# VIews to add new Complain Category
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

#View for viewing complain to normal user
@login_required
def my_complain(request):
    user=request.user
    my_complains=user.my_complains.all()
    context={
        'my_complains':my_complains
    }
    return render(request,'main/mycomplain.html',context)

#viewing individual Complain
def view_complain(request, id):
    complain=get_object_or_404(Complain, id=id)
    context={
        'complain':complain
    }
    return render(request,'main/view_complain.html',context)


#view for all complains for admin and superadmin
def all_complain(request):
    user=request.user
    if user.role == 1:
        complains=Complain.objects.all()
    elif user.role == 2:
        complains=Complain.objects.filter(to_complain__department_name = user.admin_category.department_name)
    context={
        'complains' :complains,
    }
    return render(request,'main/all_complains.html',context)

def anonymous_complain(request):
    return render(request,'main/anonymous_complains.html')

def all_user(request):
    return render(request, 'main/all_user.html')
def my_account(request):
    return render(request,'main/myaccount.html')



