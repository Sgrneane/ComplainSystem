from django.shortcuts import render, redirect
from django.urls import reverse
from . models import Complain
from .serilizer import PostSerializer
from rest_framework import generics

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def dashboard(request):
    return render(request,'main/dashboard.html')
def create_complain(request):
    if (request.method== 'POST'):
        complain_title=request.POST.get('complain_title')
        to_complain=request.POST.get('to_complain')
        complain_message=request.POST.get('complain_message')
        image=request.FILES.get('complain_image')
        Complain.objects.create(
            created_by=request.user,
            complain_title= complain_title,
            to_complain=to_complain,
            complain_message=complain_message,
            complain_image=image,
        )
        print(image)
        return redirect(reverse('main:my_complain'))
   
    return render(request,'main/create-complain.html')
def my_complain(request):
    user=request.user
    all_complains=user.my_complains.all()
    print(all_complains)
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
def view_complain(request):
    return render(request,'main/view_complain.html')

def all_complain(request):
    return render(request,'main/all_complains.html')

def anonymous_complain(request):
    return render(request,'main/anonymous_complains.html')
def my_account(request):
    return render(request,'main/myaccount.html')

class PostAPIView(generics.ListCreateAPIView):
    queryset=Complain.objects.all()
    serializer_class=PostSerializer
