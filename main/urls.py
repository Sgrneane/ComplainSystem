from django.urls import path
from . import views

app_name='main'


urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('create_complain', views.create_complain,name='create_complain'),
    path('my_account',views.my_account,name='my_account'),
    path('view_complain/<int:id>', views.view_complain, name='view_complain'),
    path('view_response/<int:id>', views.view_response, name='view_response'),
    path('all_complain', views.all_complain, name='all_complains'),
    path('add_category', views.add_category, name='add_category'),
    path('view_category', views.view_category,name='view_category'),
    path('anonymous_complain', views.anonymous_complain, name='anonymous_complains'),
    path('all_user', views.all_user, name='all_user'),
    path('complain_responses', views.complain_responses, name='complain_responses'),
    path('anonymous_form', views.anonymous_form, name="anonymous_form"),
    path("aboutus/", views.AboutUs, name='about'),
    path('privacy/',views.privacy,name='privacy')
]