from django.urls import path
from . import views

app_name='account'


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user,name='login_user'),
    path('logout/',views.logout_user, name='logout_user'),
    path('create_admin/',views.create_admin,name='create_admin'),
    path('forget_password/', views.forget_password,name='forget_password')
]