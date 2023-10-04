from django.urls import path
from . import views

app_name='main'


urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('create_complain', views.create_complain,name='create_complain'),
    path('my_complain',views.my_complain, name='my_complain'),
    path('admin_all_complains',views.admin_all_complains,name='admin_all_complains'),
    path('my_account',views.my_account,name='my_account'),
    path("complain/api",views.PostAPIView.as_view(), name="post_api"),
]