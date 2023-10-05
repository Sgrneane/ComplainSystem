from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# Register your models here.
# class CustomUser(UserAdmin):
#     list_display = ["username","email",'first_name','last_name', "username",'role','admin_category']
admin.site.register(CustomUser)
