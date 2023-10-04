from django.shortcuts import render, redirect
from django.urls import reverse

from rest_framework import generics

from . models import Complain, ComplainName
from .serilizer import PostSerializer
from .forms import ComplainForm

# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def dashboard(request):
    return render(request,'main/dashboard.html')


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


def my_complain(request):
    user=request.user
    all_complains=user.my_complains.all()
    # print(all_complains)
    context={
        'all_complains':all_complains
    }
    return render(request,'main/mycomplain.html',context)

#Rendering all complains to admin panel
def admin_all_complains(request):
    all_complains=Complain.objects.filter(to_complain=request.user.admin_category)
    context={
        'all_complains': all_complains
    }
    return render(request,'main/admin_allcomplains.html',context)
def my_account(request):
    return render(request,'main/myaccount.html')

class PostAPIView(generics.ListCreateAPIView):
    queryset=Complain.objects.all()
    serializer_class=PostSerializer
