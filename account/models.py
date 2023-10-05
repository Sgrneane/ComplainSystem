from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from . import choices

from main.models import ComplainName


class CustomUser(AbstractUser):
    username = models.CharField(max_length=255,unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=10, null=True, 
        validators=[
            RegexValidator(r'^\d{10}$', 'Phone number must be 10 digits')
        ]
    )
    created_date=models.DateTimeField(auto_now_add=True)
    role = models.PositiveSmallIntegerField(
        choices=choices.ROLE_CHOICES, blank=True, default=3
    )
    admin_category = models.ForeignKey(
        ComplainName, on_delete=models.SET_NULL, null=True
    )
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username',]
    
    def __str__(self) -> str:
        return self.email
    
    def role_name(self):
        if self.role==1:
            return 'superadmin'
        elif self.role==2:
            return 'admin'
        else:
            return 'user'
    # list_display = ["email",'first_name','last_name', "username",]